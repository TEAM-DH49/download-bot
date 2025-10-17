"""File cleanup utilities"""
import os
import logging
import asyncio

logger = logging.getLogger(__name__)

def cleanup_file(filepath):
    """Delete a single file"""
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            logger.info(f"Cleaned: {filepath}")
            return True
    except Exception as e:
        logger.error(f"Cleanup error: {e}")
        return False

def cleanup_files(filepaths):
    """Delete multiple files"""
    for filepath in filepaths:
        cleanup_file(filepath)

async def auto_cleanup(filepath, delay=60):
    """Auto delete file after delay"""
    await asyncio.sleep(delay)
    cleanup_file(filepath)

def cleanup_downloads_folder():
    """Clean entire downloads folder"""
    try:
        for file in os.listdir('downloads'):
            filepath = os.path.join('downloads', file)
            if os.path.isfile(filepath):
                os.remove(filepath)
        logger.info("Downloads folder cleaned")
    except Exception as e:
        logger.error(f"Folder cleanup error: {e}")
