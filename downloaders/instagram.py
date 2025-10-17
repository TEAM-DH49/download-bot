import yt_dlp
import instaloader
import os
import logging
import re

logger = logging.getLogger(__name__)

async def download_instagram(url):
    """Download Instagram PUBLIC posts only (no login)"""
    try:
        # Extract shortcode
        match = re.search(r'/(p|reel)/([A-Za-z0-9_-]+)', url)
        if not match:
            return {'success': False, 'error': 'Invalid Instagram URL'}

        shortcode = match.group(2)

        # Use yt-dlp WITHOUT cookies
        opts = {
            'outtmpl': f'downloads/ig_{shortcode}.%(ext)s',
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'extractor_args': {'instagram': {'login': 'false'}}
        }

        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
            fn = ydl.prepare_filename(info)

            if os.path.exists(fn):
                return {
                    'success': True,
                    'file': fn,
                    'title': info.get('title', 'Instagram')[:50],
                    'type': 'video' if info.get('ext') in ['mp4', 'webm'] else 'photo'
                }

    except Exception as e:
        error_msg = str(e)
        logger.error(f"Instagram: {error_msg}")
        
        if '401' in error_msg or 'Unauthorized' in error_msg:
            return {
                'success': False,
                'error': '⚠️ Instagram blocked the request. Please:\n1. Wait 2-3 minutes\n2. Use a PUBLIC post\n3. Try a different post'
            }
        elif 'Private' in error_msg:
            return {'success': False, 'error': '🔒 Private account. Use public posts only.'}
        else:
            return {'success': False, 'error': f'Error: {error_msg[:100]}'}
