from telegram import Update
from telegram.ext import ContextTypes
from database import db
from config import ADMIN_ID

async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_ID:
        await update.message.reply_text("❌ Admin only!")
        return
    
    total = db.get_total_users()
    today = db.get_today_users()
    downloads = db.get_total_downloads()
    
    admin_panel = f"""
👮 **ADMIN PANEL**

👥 Total Users: {total}
📅 Today's Active: {today}
📥 Total Downloads: {downloads}

🎯 Bot running smoothly!
    """
    await update.message.reply_text(admin_panel)
