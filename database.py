import os
from datetime import datetime
import sqlite3
from logger import logger

class Database:
    def __init__(self):
        try:
            self.conn = sqlite3.connect('bot_data.db', detect_types=sqlite3.PARSE_DECLTYPES)
            self.cursor = self.conn.cursor()
            self._setup_sqlite_tables()
        except sqlite3.Error as e:
            logger.error(f"SQLite initialization error: {e}")
            raise

    def _setup_sqlite_tables(self):
        self.cursor.executescript('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_seen DATETIME,
                commands_used INTEGER DEFAULT 0,
                join_date DATETIME DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS command_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                command TEXT,
                args TEXT,
                timestamp DATETIME,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            );

            CREATE TABLE IF NOT EXISTS qr_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                text_content TEXT,
                timestamp DATETIME,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            );
        ''')
        self.conn.commit()

    def add_or_update_user(self, user_id, username, first_name):
        self.cursor.execute('''
            INSERT INTO users (user_id, username, first_name, last_seen, commands_used)
            VALUES (?, ?, ?, ?, 1)
            ON CONFLICT(user_id) DO UPDATE SET
                username = ?,
                first_name = ?,
                last_seen = ?,
                commands_used = commands_used + 1
        ''', (user_id, username, first_name, datetime.now(),
              username, first_name, datetime.now()))
        self.conn.commit()

    def log_command(self, user_id, command, args):
        self.cursor.execute('''
        INSERT INTO command_history (user_id, command, args, timestamp)
        VALUES (?, ?, ?, ?)
        ''', (user_id, command, args, datetime.now()))
        self.conn.commit()

    def log_qr_generation(self, user_id, text_content):
        self.cursor.execute('''
        INSERT INTO qr_history (user_id, text_content, timestamp)
        VALUES (?, ?, ?)
        ''', (user_id, text_content, datetime.now()))
        self.conn.commit()

    def get_user_history(self, user_id):
        self.cursor.execute('''
        SELECT command, args, timestamp 
        FROM command_history 
        WHERE user_id = ? 
        ORDER BY timestamp DESC
        ''', (user_id,))
        return self.cursor.fetchall()

    def get_user_stats(self, user_id):
        try:
            self.cursor.execute('''
            SELECT 
                u.username,
                u.first_name,
                u.commands_used,
                u.join_date,
                u.last_seen,
                COUNT(DISTINCT q.id) as qr_codes_generated
            FROM users u
            LEFT JOIN qr_history q ON u.user_id = q.user_id
            WHERE u.user_id = ?
            GROUP BY u.user_id
            ''', (user_id,))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            logger.error(f"Database error in get_user_stats: {e}")
            raise

    def get_qr_history(self, user_id):
        self.cursor.execute('''
        SELECT text_content, timestamp
        FROM qr_history
        WHERE user_id = ?
        ORDER BY timestamp DESC
        ''', (user_id,))
        return self.cursor.fetchall()

    def get_all_users(self):
        self.cursor.execute('''
        SELECT user_id, username, first_name, last_seen
        FROM users
        ORDER BY last_seen DESC
        ''')
        return self.cursor.fetchall()

    def get_total_qr_codes(self):
        self.cursor.execute('SELECT COUNT(*) FROM qr_history')
        return self.cursor.fetchone()[0]

    def get_commands_today(self):
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        self.cursor.execute('''
            SELECT COUNT(*) FROM command_history 
            WHERE timestamp > ?
        ''', (today_start,))
        return self.cursor.fetchone()[0]

    def get_active_users_today(self):
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        self.cursor.execute('''
            SELECT COUNT(DISTINCT user_id) FROM users 
            WHERE last_seen > ?
        ''', (today_start,))
        return self.cursor.fetchone()[0]

    def get_stats(self):
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        self.cursor.execute('SELECT COUNT(*) FROM users')
        total_users = self.cursor.fetchone()[0]
        
        self.cursor.execute('SELECT COUNT(DISTINCT user_id) FROM users WHERE last_seen >= ?', (today,))
        active_today = self.cursor.fetchone()[0]
        
        self.cursor.execute('SELECT COUNT(*) FROM command_history WHERE timestamp >= ?', (today,))
        commands_today = self.cursor.fetchone()[0]
        
        self.cursor.execute('SELECT COUNT(*) FROM qr_history')
        total_qr_codes = self.cursor.fetchone()[0]
        
        return {
            "total_users": total_users,
            "active_today": active_today,
            "commands_today": commands_today,
            "total_qr_codes": total_qr_codes
        }