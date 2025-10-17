import yt_dlp
import os
import logging
import ssl

logger = logging.getLogger(__name__)

async def download_tiktok(url):
    """Download TikTok - SSL bypass for India"""
    try:
        opts = {
            'outtmpl': 'downloads/tiktok_%(id)s.%(ext)s',
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
            'nocheckcertificate': True,  # SSL bypass
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Referer': 'https://www.tiktok.com/'
            }
        }
        
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get('title', 'TikTok')
            fn = ydl.prepare_filename(info)
            
            if os.path.exists(fn):
                return {'success': True, 'file': fn, 'title': title}
        
        return {'success': False, 'error': 'Download failed'}
        
    except Exception as e:
        error_msg = str(e)
        
        # India ban detection
        if 'CERTIFICATE' in error_msg or 'SSL' in error_msg:
            return {
                'success': False, 
                'error': 'TikTok blocked in India. Use VPN or try Instagram Reels instead!'
            }
        elif 'Video not available' in error_msg:
            return {'success': False, 'error': 'Video unavailable or private'}
        else:
            logger.error(f"TikTok: {e}")
            return {'success': False, 'error': str(e)[:150]}
