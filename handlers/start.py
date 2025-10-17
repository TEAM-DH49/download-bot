from telegram import Update
from telegram.ext import ContextTypes
from database import add_user

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    add_user(user.id, user.username)
    
    welcome_message = """╔══════════════════════════╗
   MEDIA DOWNLOADER BOT
      Professional Edition
╚══════════════════════════╝

Hello! I'm your intelligent media extraction assistant, designed to deliver high-quality content from multiple platforms instantly.

───────────────────────────
📊 SUPPORTED PLATFORMS

✓ YouTube
  • Videos & Shorts
  • Multiple quality options (1080p/720p/480p)
  • Audio extraction (MP3)

✓ Instagram  
  • Posts, Reels & Stories
  • Photos & Videos
  • HD quality preservation

✓ Twitter/X
  • All media types supported

✓ Facebook
  • Video downloads

✓ Thumbnails
  • High-resolution extraction

───────────────────────────
⚙️ USAGE INSTRUCTIONS

Send any supported platform link
Download begins automatically
Receive your media in seconds

───────────────────────────
🎯 FEATURES

• No registration required
• Unlimited downloads
• Fast processing
• HD quality
• Secure & private

Bot statistics: /stats

━━━━━━━━━━━━━━━━━━━━━━━
Powered by TEAM DH 49
Version 2.0 | 24/7 Uptime
━━━━━━━━━━━━━━━━━━━━━━━"""

    await update.message.reply_text(welcome_message)
