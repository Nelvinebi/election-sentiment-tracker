"""
SQLite database operations. Handles all CRUD for daily metrics.
"""

import sqlite3
import pandas as pd
from src.config import DB_PATH


def init_db():
    """Create the database and table if they don't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_metrics (
            date TEXT PRIMARY KEY,
            Tinubu_mentions INTEGER,
            Tinubu_sentiment REAL,
            Tinubu_positive REAL,
            Tinubu_negative REAL,
            Tinubu_neutral REAL,
            Obi_mentions INTEGER,
            Obi_sentiment REAL,
            Obi_positive REAL,
            Obi_negative REAL,
            Obi_neutral REAL,
            Atiku_mentions INTEGER,
            Atiku_sentiment REAL,
            Atiku_positive REAL,
            Atiku_negative REAL,
            Atiku_neutral REAL,
            collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"✅ Database initialized at {DB_PATH}")


def save_daily_data(data: dict):
    """Insert a day's data. Updates if date already exists."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    columns = ', '.join(data.keys())
    placeholders = ', '.join(['?' for _ in data])
    
    cursor.execute(f'''
        INSERT OR REPLACE INTO daily_metrics ({columns})
        VALUES ({placeholders})
    ''', tuple(data.values()))
    
    conn.commit()
    conn.close()


def get_all_data() -> pd.DataFrame:
    """Return all historical data as a DataFrame."""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql('SELECT * FROM daily_metrics ORDER BY date', conn)
    conn.close()
    return df


def get_latest_date() -> str:
    """Return the most recent date in the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT MAX(date) FROM daily_metrics')
    result = cursor.fetchone()[0]
    conn.close()
    return result
