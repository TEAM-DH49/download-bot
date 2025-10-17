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
