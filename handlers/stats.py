from telegram import Update
from telegram.ext import ContextTypes
from database import db

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    total = db.get_total_users()
    today = db.get_today_users()
    downloads = db.get_total_downloads()
    
    stats = f"""
📊 **BOT STATISTICS**

👥 Total Users: {total}
📅 Today's Users: {today}
📥 Total Downloads: {downloads}

✨ Thank you for using our bot!
    """
    await update.message.reply_text(stats)
