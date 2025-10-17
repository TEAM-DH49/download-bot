from telegram import Update
from telegram.ext import ContextTypes

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = """
⭐ **PREMIUM DOWNLOADER** ⭐

👋 Welcome TEAM DH 49!

🎯 **AVAILABLE COMMANDS:**

📺 /youtube <link> - YouTube Videos
   → 720p/480p/Max/MP3

📸 /instagram <link> - Instagram Reels
   → Videos & Reels only
   → 📸 Photos coming soon!

🐦 /twitter <link> - Twitter Videos
🎵 /facebook <link> - Facebook Videos
🖼️ /thumbnail <link> - YouTube Thumbnails

📊 /stats - Bot Statistics

⚡ Fast • Reliable • HD Quality
    """
    
    await update.message.reply_text(welcome_text)
