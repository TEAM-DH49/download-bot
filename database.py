"""Database for stats"""
import sqlite3
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class Database:
    def __init__(self, db_file='bot_stats.db'):
        self.db_file = db_file
        self.init_db()
    
    def get_conn(self):
        return sqlite3.connect(self.db_file)
    
    def init_db(self):
        conn = self.get_conn()
        c = conn.cursor()
        
        c.execute('''CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            download_count INTEGER DEFAULT 0
        )''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS downloads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            platform TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        conn.commit()
        conn.close()
        logger.info("✅ Database initialized")
    
    def add_user(self, user_id, username=None):
        conn = self.get_conn()
        c = conn.cursor()
        c.execute('INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)', (user_id, username))
        c.execute('UPDATE users SET last_active = ? WHERE user_id = ?', (datetime.now(), user_id))
        conn.commit()
        conn.close()
    
    def add_download(self, user_id, platform):
        conn = self.get_conn()
        c = conn.cursor()
        c.execute('INSERT INTO downloads (user_id, platform) VALUES (?, ?)', (user_id, platform))
        c.execute('UPDATE users SET download_count = download_count + 1 WHERE user_id = ?', (user_id,))
        conn.commit()
        conn.close()
    
    def get_total_users(self):
        conn = self.get_conn()
        c = conn.cursor()
        c.execute('SELECT COUNT(*) FROM users')
        count = c.fetchone()[0]
        conn.close()
        return count
    
    def get_today_users(self):
        conn = self.get_conn()
        c = conn.cursor()
        c.execute('SELECT COUNT(DISTINCT user_id) FROM downloads WHERE DATE(created_at) = DATE("now")')
        count = c.fetchone()[0]
        conn.close()
        return count
    
    def get_total_downloads(self):
        conn = self.get_conn()
        c = conn.cursor()
        c.execute('SELECT COUNT(*) FROM downloads')
        count = c.fetchone()[0]
        conn.close()
        return count
    
    def get_platform_stats(self):
        conn = self.get_conn()
        c = conn.cursor()
        c.execute('SELECT platform, COUNT(*) FROM downloads GROUP BY platform')
        stats = c.fetchall()
        conn.close()
        return stats

db = Database()
