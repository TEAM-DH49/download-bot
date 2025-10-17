from telegram import Update
from telegram.ext import ContextTypes

async def tiktok_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = """
🚫 **TikTok Not Available in India**

TikTok has been banned in India since June 2020 and is completely blocked by ISPs.

✅ **Try These Popular Alternatives:**

📸 **Instagram Reels** (Most Popular!)
Usage: `/instagram <reel_link>`
Example: `/instagram https://www.instagram.com/reel/ABC123/`

📺 **YouTube Shorts**
Usage: `/youtube <shorts_link>`
Example: `/youtube https://youtube.com/shorts/ABC123`

📘 **Facebook Reels**
Usage: `/facebook <reel_link>`

🐦 **Twitter Videos**
Usage: `/twitter <tweet_link>`

---
💡 **For International Users:**
TikTok download requires VPN connection. The bot cannot access TikTok from India.
    """
    
    await update.message.reply_text(message, parse_mode='Markdown')
