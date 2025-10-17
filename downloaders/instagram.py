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
        
        # Try yt-dlp first (faster for videos)
        try:
            opts = {
                'outtmpl': f'downloads/ig_{shortcode}.%(ext)s',
                'format': 'best',
                'quiet': True,
                'no_warnings': True,
            }
            
            cookies_file = 'instagram_cookies.txt'
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
            # If yt-dlp fails, try instaloader for photos
            logger.info("yt-dlp failed, trying instaloader for photo...")
            
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
            
            # Load session from cookies
            cookies_file = 'instagram_cookies.txt'
            if os.path.exists(cookies_file):
                try:
                    with open(cookies_file, 'r') as f:
                        for line in f:
                            if 'sessionid' in line and not line.startswith('#'):
                                sessionid = line.strip().split('\t')[-1]
                                L.context._session.cookies.set('sessionid', sessionid, domain='.instagram.com')
                                break
                except:
                    pass
            
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
        return {'success': False, 'error': 'Private post - cookies may be expired'}
    except instaloader.exceptions.ProfileNotExistsException:
        return {'success': False, 'error': 'Post not found or deleted'}
    except Exception as e:
        logger.error(f"Instagram: {e}")
        return {'success': False, 'error': str(e)[:150]}
