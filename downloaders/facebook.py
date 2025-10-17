import yt_dlp, os

async def download_facebook(url):
    try:
        opts = {'outtmpl': 'downloads/%(title)s.%(ext)s', 'quiet': True, 'format': 'best'}
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
            fn = ydl.prepare_filename(info)
            return {'success': True, 'file': fn, 'type': 'video'}
    except Exception as e:
        return {'success': False, 'error': str(e)[:200]}
