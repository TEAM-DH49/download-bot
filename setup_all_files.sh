#!/bin/bash
# Complete bot setup - All files

echo "🚀 Setting up Telegram Bot files..."

cd ~/premium_downloader_bot

# ============================================
# 1. KEEP_ALIVE.PY
# ============================================
cat > keep_alive.py << 'KEEPALIVE'
from aiohttp import web
import asyncio
import logging
import os

logger = logging.getLogger(__name__)

async def health_check(request):
    """Health check endpoint for Render"""
    return web.Response(text="Bot is alive! ✅")

async def start_web_server():
    """Start HTTP server on port 8080 for Render"""
    app = web.Application()
    app.router.add_get('/', health_check)
    app.router.add_get('/health', health_check)
    
    runner = web.AppRunner(app)
    await runner.setup()
    
    port = int(os.environ.get('PORT', 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    
    logger.info(f"🌐 Web server started on port {port}")

def run_server():
    """Run web server in separate thread"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_web_server())
    loop.run_forever()
KEEPALIVE

echo "✅ keep_alive.py created"

# ============================================
# 2. REQUIREMENTS.TXT
# ============================================
cat > requirements.txt << 'REQUIREMENTS'
python-telegram-bot==21.0
yt-dlp
instaloader
aiohttp
requests
REQUIREMENTS

echo "✅ requirements.txt created"

# ============================================
# 3. RENDER.YAML
# ============================================
cat > render.yaml << 'RENDERYAML'
services:
  - type: web
    name: telegram-downloader-bot
    runtime: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: python main.py
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
RENDERYAML

echo "✅ render.yaml created"

# ============================================
# 4. .GITIGNORE
# ============================================
cat > .gitignore << 'GITIGNORE'
config.py
instagram_cookies.txt
*.db
downloads/
__pycache__/
*.pyc
.env
.DS_Store
GITIGNORE

echo "✅ .gitignore created"

# ============================================
# 5. README.MD
# ============================================
cat > README.md << 'README'
# 🎬 Telegram Video Downloader Bot

Premium multi-platform downloader bot

## Features
- ✅ YouTube (multi-quality)
- ✅ Instagram (photos + videos)
- ✅ Facebook videos
- ✅ Twitter videos
- ✅ Statistics tracking

## Deploy on Render
1. Fork this repo
2. Sign up on Render.com
3. Create Web Service
4. Deploy!

## Keep Awake
Use UptimeRobot to ping every 5 minutes

## License
MIT
README

echo "✅ README.md created"

# ============================================
# 6. CONFIG TEMPLATE
# ============================================
cat > config_template.py << 'CONFIGTEMPLATE'
# Bot Configuration Template
# Copy this to config.py and fill in your details

BOT_TOKEN = "YOUR_BOT_TOKEN_FROM_BOTFATHER"
ADMIN_ID = 123456789  # Your Telegram user ID from @userinfobot
CONFIGTEMPLATE

echo "✅ config_template.py created"

# ============================================
# 7. UPDATE MAIN.PY
# ============================================
# Backup existing main.py
cp main.py main.py.backup 2>/dev/null

# Add web server import to main.py if not exists
if ! grep -q "from keep_alive import run_server" main.py; then
    # Add before if __name__ == '__main__':
    sed -i "/if __name__ == '__main__':/i\\
# Start web server for Render\\
from keep_alive import run_server\\
import threading\\
server_thread = threading.Thread(target=run_server, daemon=True)\\
server_thread.start()\\
" main.py
    echo "✅ main.py updated with web server"
else
    echo "✅ main.py already has web server"
fi

# ============================================
# 8. CREATE DOWNLOADS FOLDER
# ============================================
mkdir -p downloads
touch downloads/.gitkeep

echo ""
echo "🎉 🎉 🎉 ALL FILES CREATED! 🎉 🎉 🎉"
echo ""
echo "📁 Created files:"
echo "   ✅ keep_alive.py"
echo "   ✅ requirements.txt"
echo "   ✅ render.yaml"
echo "   ✅ .gitignore"
echo "   ✅ README.md"
echo "   ✅ config_template.py"
echo "   ✅ downloads/ folder"
echo ""
echo "⚠️  NEXT STEPS:"
echo "1. Create config.py:"
echo "   cp config_template.py config.py"
echo "   nano config.py  # Add your BOT_TOKEN"
echo ""
echo "2. Test locally:"
echo "   python3 main.py"
echo ""
echo "3. Deploy to GitHub:"
echo "   git init"
echo "   git add ."
echo "   git commit -m 'Initial commit'"
echo "   git push"
echo ""
echo "4. Deploy on Render.com!"
echo ""
