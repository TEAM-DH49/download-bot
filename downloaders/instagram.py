import yt_dlp
import instaloader
import os
import logging
import re
import glob

logger = logging.getLogger(__name__)

async def download_instagram(url):
    """Instagram - Photos + Videos + Reels + Fresh Cookies"""
    try:
        match = re.search(r'/(p|reel)/([A-Za-z0-9_-]+)', url)
        if not match:
            return {'success': False, 'error': 'Invalid Instagram URL'}

        shortcode = match.group(2)
        
        # Try yt-dlp first (videos/reels)
        try:
            opts = {
                'outtmpl': f'downloads/ig_{shortcode}.%(ext)s',
                'format': 'best',
                'quiet': True,
                'no_warnings': True,
            }

            cookies_file = 'cookies/instagram.com_cookies.txt'
            if os.path.exists(cookies_file):
                opts['cookiefile'] = cookies_file
                logger.info("✅ Using fresh Instagram cookies")

            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=True)
                fn = ydl.prepare_filename(info)

                if os.path.exists(fn):
                    return {
                        'success': True,
                        'file': fn,
                        'title': info.get('title', 'Instagram')[:50],
                        'type': 'video' if fn.endswith('.mp4') else 'photo'
                    }
        except Exception as e:
            logger.info(f"yt-dlp failed, trying instaloader: {e}")

        # Fallback: instaloader (photos/carousels)
        L = instaloader.Instaloader(
            dirname_pattern='downloads',
            filename_pattern='{shortcode}',
            download_videos=True,
            download_video_thumbnails=False,
            download_geotags=False,
            download_comments=False,
            save_metadata=False,
            compress_json=False,
            quiet=True
        )

        # Load fresh cookies
        cookies_file = 'cookies/instagram.com_cookies.txt'
        if os.path.exists(cookies_file):
            with open(cookies_file, 'r') as f:
                for line in f:
                    if 'sessionid' in line and not line.startswith('#'):
                        sessionid = line.strip().split('\t')[-1]
                        L.context._session.cookies.set('sessionid', sessionid, domain='.instagram.com')
                        logger.info("✅ Loaded fresh Instagram session")
                        break

        post = instaloader.Post.from_shortcode(L.context, shortcode)
        L.download_post(post, target='downloads')

        files = glob.glob(f'downloads/{shortcode}*')
        if files:
            first = files[0]
            return {
                'success': True,
                'file': first,
                'title': (post.caption or 'Instagram')[:50],
                'type': 'video' if first.endswith('.mp4') else 'photo'
            }

        return {'success': False, 'error': 'Download failed'}

    except Exception as e:
        logger.error(f"Instagram: {e}")
        if '401' in str(e):
            return {'success': False, 'error': '⚠️ Rate limited. Wait 2 minutes.'}
        return {'success': False, 'error': str(e)[:100]}
