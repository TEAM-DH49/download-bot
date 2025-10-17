import yt_dlp
import instaloader
import os
import logging
import re

logger = logging.getLogger(__name__)

async def download_instagram(url):
    """Download Instagram Photos + Videos + Reels"""
    try:
        # Extract shortcode from URL
        match = re.search(r'/(p|reel)/([A-Za-z0-9_-]+)', url)
        if not match:
            return {'success': False, 'error': 'Invalid Instagram URL'}

        shortcode = match.group(2)

        # Try yt-dlp first (faster for videos) - WITHOUT COOKIES
        try:
            opts = {
                'outtmpl': f'downloads/ig_{shortcode}.%(ext)s',
                'format': 'best',
                'quiet': True,
                'no_warnings': True,
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }

            # Try with cookies first
            cookies_file = 'cookies/instagram.com_cookies.txt'
            if os.path.exists(cookies_file):
                opts['cookiefile'] = cookies_file

            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=True)
                fn = ydl.prepare_filename(info)

                if os.path.exists(fn):
                    return {
                        'success': True,
                        'file': fn,
                        'title': info.get('title', 'Instagram')[:50],
                        'type': 'video'
                    }
        except Exception as video_error:
            logger.info(f"yt-dlp failed: {video_error}, trying instaloader...")

            # If yt-dlp fails, try instaloader WITHOUT LOGIN
            try:
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

                # Try to load cookies if available
                cookies_file = 'cookies/instagram.com_cookies.txt'
                if os.path.exists(cookies_file):
                    try:
                        with open(cookies_file, 'r') as f:
                            for line in f:
                                if 'sessionid' in line and not line.startswith('#'):
                                    sessionid = line.strip().split('\t')[-1]
                                    L.context._session.cookies.set('sessionid', sessionid, domain='.instagram.com')
                                    break
                    except Exception as cookie_error:
                        logger.info(f"Cookie loading failed: {cookie_error}")

                # Download post
                post = instaloader.Post.from_shortcode(L.context, shortcode)
                L.download_post(post, target='')

                # Find downloaded file
                for ext in ['.jpg', '.jpeg', '.png', '.mp4']:
                    filepath = f'downloads/{shortcode}{ext}'
                    if os.path.exists(filepath):
                        file_type = 'video' if ext == '.mp4' else 'photo'
                        return {
                            'success': True,
                            'file': filepath,
                            'title': (post.caption[:50] if post.caption else 'Instagram')[:50],
                            'type': file_type
                        }

                return {'success': False, 'error': 'File not found after download'}
            
            except instaloader.exceptions.LoginRequiredException:
                return {
                    'success': False, 
                    'error': '🔒 Private post. Try a public Instagram post or wait a few minutes.'
                }
            except instaloader.exceptions.ProfileNotExistsException:
                return {'success': False, 'error': 'Post not found or deleted'}

    except Exception as e:
        logger.error(f"Instagram error: {e}")
        error_msg = str(e)
        
        # Better error messages
        if '401' in error_msg or 'Unauthorized' in error_msg:
            return {
                'success': False,
                'error': '⚠️ Instagram rate limit. Please wait 2-3 minutes and try again with a public post.'
            }
        elif 'Private' in error_msg or 'login' in error_msg.lower():
            return {
                'success': False,
                'error': '🔒 This is a private account. Please use a public post URL.'
            }
        else:
            return {'success': False, 'error': f'Error: {str(e)[:100]}'}
