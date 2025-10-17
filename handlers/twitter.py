from telegram import Update
from telegram.ext import ContextTypes
from downloaders.twitter import download_twitter
from database import db
import asyncio, os

async def twitter_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /twitter <link>")
        return
    
    url = context.args[0]
    msg = await update.message.reply_text("⏳ Downloading...")
    
    result = await download_twitter(url)
    
    if not result['success']:
        await msg.edit_text(f"❌ Failed!\n\n{result['error']}")
        return
    
    try:
        filepath = result['file']
        with open(filepath, 'rb') as f:
            if result['type'] == 'photo':
                await context.bot.send_photo(chat_id=update.effective_chat.id, photo=f, caption="✅ Twitter")
            else:
                await context.bot.send_video(chat_id=update.effective_chat.id, video=f, caption="✅ Twitter", supports_streaming=True)
        
        await msg.delete()
        db.add_download(update.effective_user.id, 'twitter')
        
        await asyncio.sleep(60)
        if os.path.exists(filepath):
            os.remove(filepath)
    except Exception as e:
        await msg.edit_text(f"❌ Failed!\n\n{str(e)[:150]}")
        if os.path.exists(filepath):
            os.remove(filepath)
