from telegram import Update
from telegram.ext import ContextTypes
from downloaders.instagram import download_instagram
from database import db
import os
import asyncio

async def instagram_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "📸 Instagram Downloader\n\n"
            "✅ Photos, Videos & Reels\n"
            "✅ Private posts (with cookies)\n\n"
            "Usage: `/instagram <link>`"
        )
        return
    
    url = context.args[0]
    msg = await update.message.reply_text("⚡ Downloading from Instagram...")
    
    result = await download_instagram(url)
    
    if not result['success']:
        await msg.edit_text(f"❌ {result['error']}")
        return
    
    filepath = result['file']
    title = result.get('title', 'Instagram')[:50]
    file_size = os.path.getsize(filepath) / (1024 * 1024)
    content_type = result.get('type', 'video')
    
    if file_size > 2048:
        await msg.edit_text(f"❌ Too large: {file_size:.0f}MB")
        os.remove(filepath)
        return
    
    try:
        await msg.edit_text(f"📤 Uploading...")
        
        with open(filepath, 'rb') as f:
            if content_type == 'photo':
                # Send as photo
                await context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=f,
                    caption=f"✅ {title}"
                )
            else:
                # Send as video
                await context.bot.send_video(
                    chat_id=update.effective_chat.id,
                    video=f,
                    caption=f"✅ {title}",
                    supports_streaming=True
                )
        
        await msg.delete()
        db.add_download(update.effective_user.id, 'instagram')
        
        await asyncio.sleep(60)
        if os.path.exists(filepath):
            os.remove(filepath)
        
    except Exception as e:
        await msg.edit_text(f"❌ {str(e)[:150]}")
        if os.path.exists(filepath):
            os.remove(filepath)
