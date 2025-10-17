import yt_dlp
import os
import logging

logger = logging.getLogger(__name__)

async def get_youtube_link(url, quality='720p'):
    """Get direct download link with PROPER quality selection"""
    try:
        # PROPER format selection - separate video + audio
        format_map = {
            '360p': 'bestvideo[height=360][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=360]+bestaudio/best[height<=360]',
            '480p': 'bestvideo[height=480][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=480]+bestaudio/best[height<=480]',
            '720p': 'bestvideo[height=720][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=720]+bestaudio/best[height<=720]',
            '1080p': 'bestvideo[height=1080][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=1080]+bestaudio/best[height<=1080]',
            'max': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best',
        }
        
        opts = {
            'format': format_map.get(quality, 'best'),
            'quiet': True,
            'no_warnings': True,
            'skip_download': True,
            'nocheckcertificate': True,
        }
        
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            title = info.get('title', 'YouTube Video')
            duration = info.get('duration', 0)
            thumbnail = info.get('thumbnail')
            
            # Get format info
            format_id = info.get('format_id', '')
            resolution = info.get('resolution', 'Unknown')
            vcodec = info.get('vcodec', 'Unknown')
            acodec = info.get('acodec', 'Unknown')
            
            # Calculate filesize
            filesize = info.get('filesize') or info.get('filesize_approx', 0)
            
            # If filesize not available, estimate from duration and quality
            if not filesize and duration:
                bitrate_map = {
                    '360p': 1.5,   # 1.5 Mbps
                    '480p': 2.5,   # 2.5 Mbps
                    '720p': 5,     # 5 Mbps
                    '1080p': 8,    # 8 Mbps
                    'max': 12      # 12 Mbps
                }
                bitrate = bitrate_map.get(quality, 5)
                filesize = int((duration * bitrate * 1024 * 1024) / 8)  # bytes
            
            filesize_mb = filesize / (1024 * 1024) if filesize else 0
            
            # Get direct download URL
            if 'url' in info:
                download_url = info['url']
            elif 'requested_downloads' in info and info['requested_downloads']:
                # Merged format
                download_url = info['requested_downloads'][0]['url']
            elif 'formats' in info and info['formats']:
                download_url = info['formats'][-1].get('url')
            else:
                return {'success': False, 'error': 'No download URL found'}
            
            # Quality verification
            actual_height = info.get('height', 0)
            expected_heights = {
                '360p': 360,
                '480p': 480,
                '720p': 720,
                '1080p': 1080,
                'max': 2160
            }
            
            expected = expected_heights.get(quality, 720)
            
            # Warn if quality is lower than expected
            if actual_height < expected * 0.8:  # Allow 20% tolerance
                logger.warning(f"Quality mismatch: Expected {quality}, got {actual_height}p")
            
            return {
                'success': True,
                'url': download_url,
                'title': title,
                'duration': duration,
                'thumbnail': thumbnail,
                'quality': quality,
                'actual_quality': f"{actual_height}p",
                'filesize_mb': filesize_mb,
                'format_id': format_id,
                'resolution': resolution
            }
        
    except Exception as e:
        logger.error(f"YouTube link extraction: {e}")
        return {'success': False, 'error': str(e)[:150]}


async def download_youtube(url, quality='mp3'):
    """Download MP3 only"""
    try:
        opts = {
            'outtmpl': 'downloads/yt_%(id)s.%(ext)s',
            'format': 'bestaudio/best',
            'quiet': True,
            'no_warnings': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        }
        
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get('title', 'audio')
            fn = ydl.prepare_filename(info)
            fn = fn.rsplit('.', 1)[0] + '.mp3'
            
            if os.path.exists(fn):
                return {'success': True, 'file': fn, 'title': title}
        
        return {'success': False, 'error': 'Download failed'}
        
    except Exception as e:
        logger.error(f"YouTube: {e}")
        return {'success': False, 'error': str(e)[:150]}


async def get_thumbnail(url):
    """Get YouTube thumbnail"""
    try:
        opts = {'quiet': True, 'skip_download': True}
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=False)
            thumbnail = info.get('thumbnail')
            title = info.get('title', 'YouTube Video')
            if thumbnail:
                return {'success': True, 'url': thumbnail, 'title': title}
        return {'success': False, 'error': 'No thumbnail'}
    except Exception as e:
        return {'success': False, 'error': str(e)[:100]}
