from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from handlers import start, youtube, instagram, twitter, tiktok, facebook, thumbnail, stats, admin
from config import BOT_TOKEN
import logging
import os
import time
import threading

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def check_cookie_expiry():
    """Check Instagram cookie expiry on bot start"""
    cookie_file = 'instagram_cookies.txt'
    
    if not os.path.exists(cookie_file):
        logger.warning("⚠️ No Instagram cookies found - only public posts will work")
        return
    
    try:
        with open(cookie_file, 'r') as f:
            for line in f:
                if 'sessionid' in line and not line.startswith('#'):
                    parts = line.strip().split('\t')
                    if len(parts) >= 5:
                        expiry = int(parts[4])
                        days_left = (expiry - time.time()) / 86400
                        
                        if days_left < 30:
                            logger.warning(f"⚠️ Instagram cookies expire in {days_left:.0f} days - refresh soon!")
                        elif days_left < 365:
                            logger.info(f"✅ Instagram cookies valid for {days_left:.0f} days")
                        else:
                            logger.info(f"✅ Instagram cookies valid for {days_left/365:.1f} years")
                    break
    except Exception as e:
        logger.error(f"Cookie check failed: {e}")

def main():
    # Check cookies on startup
    check_cookie_expiry()
    
    app = (
        Application.builder()
        .token(BOT_TOKEN)
        .concurrent_updates(True)
        .connection_pool_size(10)
        .read_timeout(600)
        .write_timeout(600)
        .connect_timeout(60)
        .pool_timeout(60)
        .build()
    )

    # Command handlers
    app.add_handler(CommandHandler("start", start.start_command))
    app.add_handler(CommandHandler("youtube", youtube.youtube_command))
    app.add_handler(CommandHandler("instagram", instagram.instagram_command))
    app.add_handler(CommandHandler("twitter", twitter.twitter_command))
    app.add_handler(CommandHandler("tiktok", tiktok.tiktok_command))
    app.add_handler(CommandHandler("facebook", facebook.facebook_command))
    app.add_handler(CommandHandler("thumbnail", thumbnail.thumbnail_command))
    app.add_handler(CommandHandler("stats", stats.stats_command))
    app.add_handler(CommandHandler("admin", admin.admin_command))

    # Callback handlers
    app.add_handler(CallbackQueryHandler(youtube.youtube_callback, pattern='^yt_'))

    logger.info("🚀 Bot started - ALL SYSTEMS READY!")
    app.run_polling(drop_pending_updates=True)

# Start web server in background (for Render)
from keep_alive import run_server
server_thread = threading.Thread(target=run_server, daemon=True)
server_thread.start()

if __name__ == '__main__':
    main()
