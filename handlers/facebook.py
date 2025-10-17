from telegram import Update
from telegram.ext import ContextTypes
from downloaders.facebook import download_facebook
from database import db
import os
import asyncio

async def facebook_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("📘 Facebook Downloader\n\nUsage: /facebook <link>")
        return
    
    url = context.args[0]
    
    # Direct download - no preview
    msg = await update.message.reply_text("⚡ Downloading Facebook video...")
    
    result = await download_facebook(url)
    
    if not result['success']:
        await msg.edit_text(f"❌ {result['error']}")
        return
    
    filepath = result['file']
    title = result.get('title', 'Facebook Video')[:50]
    file_size = os.path.getsize(filepath) / (1024 * 1024)
    
    if file_size > 2048:
        await msg.edit_text(f"❌ Too large: {file_size:.0f}MB")
        os.remove(filepath)
        return
    
    try:
        await msg.edit_text(f"📤 Uploading {file_size:.0f}MB...")
        
        with open(filepath, 'rb') as f:
            await context.bot.send_video(
                chat_id=update.effective_chat.id,
                video=f,
                caption=f"✅ {title}\n📦 {file_size:.0f}MB",
                supports_streaming=True,
                read_timeout=180,
                write_timeout=180,
                connect_timeout=120
            )
        
        await msg.delete()
        db.add_download(update.effective_user.id, 'facebook')
        
        # Cleanup
        asyncio.create_task(cleanup_file(filepath))
        
    except Exception as e:
        await msg.edit_text(f"❌ Upload failed: {str(e)[:150]}")
        if os.path.exists(filepath):
            os.remove(filepath)

async def cleanup_file(filepath):
    await asyncio.sleep(60)
    if os.path.exists(filepath):
        os.remove(filepath)
