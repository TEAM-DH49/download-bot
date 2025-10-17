"""Helper functions"""
import os
import logging

logger = logging.getLogger(__name__)

def format_filesize(bytes):
    """Convert bytes to readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes < 1024.0:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024.0
    return f"{bytes:.2f} TB"

def get_file_extension(filename):
    """Get file extension"""
    return os.path.splitext(filename)[1].lower()

def is_video_file(filename):
    """Check if file is video"""
    video_exts = ['.mp4', '.mkv', '.avi', '.mov', '.flv', '.webm']
    return get_file_extension(filename) in video_exts

def is_audio_file(filename):
    """Check if file is audio"""
    audio_exts = ['.mp3', '.m4a', '.wav', '.flac', '.ogg']
    return get_file_extension(filename) in audio_exts

def is_photo_file(filename):
    """Check if file is photo"""
    photo_exts = ['.jpg', '.jpeg', '.png', '.webp', '.gif']
    return get_file_extension(filename) in photo_exts

def sanitize_filename(filename):
    """Remove invalid characters from filename"""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename[:200]  # Limit length

def ensure_folder_exists(folder_path):
    """Create folder if doesn't exist"""
    os.makedirs(folder_path, exist_ok=True)
