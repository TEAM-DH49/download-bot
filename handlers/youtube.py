from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from downloaders.youtube import get_youtube_link, download_youtube
from database import db
import asyncio, os, hashlib

url_cache = {}

async def youtube_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "📺 **YouTube Downloader**\n\n"
            "Usage: /youtube <link>\n\n"
            "⚡ Instant download links!"
        )
        return
    
    url = context.args[0]
    url_id = hashlib.md5(url.encode()).hexdigest()[:8]
    url_cache[url_id] = url
    
    keyboard = [
        [
            InlineKeyboardButton("📱 360p", callback_data=f"yt_360p_{url_id}"),
            InlineKeyboardButton("📹 480p", callback_data=f"yt_480p_{url_id}")
        ],
        [
            InlineKeyboardButton("🎥 720p", callback_data=f"yt_720p_{url_id}"),
            InlineKeyboardButton("🔥 1080p", callback_data=f"yt_1080p_{url_id}")
        ],
        [
            InlineKeyboardButton("💎 Max Quality", callback_data=f"yt_max_{url_id}")
        ],
        [
            InlineKeyboardButton("🎵 MP3", callback_data=f"yt_mp3_{url_id}")
        ]
    ]
    
    await update.message.reply_text(
        "📺 **Select Quality:**",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def youtube_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    try:
        parts = query.data.split('_')
        quality, url_id = parts[1], parts[2]
        url = url_cache.get(url_id)
        
        if not url:
            await query.edit_message_text("❌ Link expired!")
            return
        
        if quality == 'mp3':
            msg = await query.edit_message_text(f"⚡ Downloading MP3...")
            result = await download_youtube(url, 'mp3')
            
            if not result['success']:
                await msg.edit_text(f"❌ {result['error']}")
                return
            
            filepath = result['file']
            title = result.get('title', 'YouTube')[:50]
            
            try:
                await msg.edit_text("📤 Uploading MP3...")
                with open(filepath, 'rb') as f:
                    await context.bot.send_audio(
                        chat_id=query.message.chat_id,
                        audio=f,
                        title=title,
                        read_timeout=120,
                        write_timeout=120
                    )
                await msg.delete()
                db.add_download(query.from_user.id, 'youtube')
                os.remove(filepath)
            except Exception as e:
                await msg.edit_text(f"❌ {str(e)[:150]}")
                if os.path.exists(filepath):
                    os.remove(filepath)
        
        else:
            msg = await query.edit_message_text("⚡ Extracting link...")
            
            result = await get_youtube_link(url, quality)
            
            if not result['success']:
                await msg.edit_text(f"❌ {result['error']}")
                return
            
            title = result['title']
            download_url = result['url']
            duration_min = result['duration'] // 60
            filesize_mb = result.get('filesize_mb', 0)
            actual_quality = result.get('actual_quality', quality)
            
            response = (
                f"✅ **{title[:40]}**\n\n"
                f"📊 Requested: **{quality.upper()}**\n"
                f"✨ Actual: **{actual_quality}**\n"
                f"📦 Size: **~{filesize_mb:.0f}MB**\n"
                f"⏱️ Duration: **{duration_min} min**\n\n"
                f"🔗 Click button below to download\n"
                f"⚠️ Link valid for 6 hours"
            )
            
            keyboard = [[
                InlineKeyboardButton("📥 Download Video", url=download_url)
            ]]
            
            await msg.edit_text(
                response,
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode='Markdown'
            )
            
            db.add_download(query.from_user.id, 'youtube')
            
            if url_id in url_cache:
                del url_cache[url_id]
            
    except Exception as e:
        await query.edit_message_text(f"❌ Error: {str(e)[:150]}")

