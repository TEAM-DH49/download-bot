from telegram import Update
from telegram.ext import ContextTypes
from downloaders.youtube import get_thumbnail

async def thumbnail_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /thumbnail <youtube_link>")
        return
    result = await get_thumbnail(context.args[0])
    if not result['success']:
        await update.message.reply_text(f"❌ Failed!\n\n{result['error']}")
        return
    await update.message.reply_photo(photo=result['url'], caption=f"✅ {result['title']}")
