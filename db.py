import sqlite3
from datetime import datetime, timedelta

DB_NAME = "db.sqlite3"

# create table
def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()

# add event (in/out)
def add_event(event_type):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO events (type) VALUES (?)", (event_type,))
        conn.commit()

# get stat by hours (for today)
def get_daily_stats():
    now = datetime.now()
    start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT strftime('%H', timestamp) as hour, COUNT(*) 
            FROM events 
            WHERE timestamp >= ? AND type = 'in'
            GROUP BY hour
        """, (start,))
        rows = cursor.fetchall()
    # transform into a list of 16 intervals
    hours = [f"{h}–{int(h)+1}" for h in range(6, 22)]
    values = [0 for _ in hours]
    for hour, count in rows:
        idx = int(hour) - 6
        if 0 <= idx < len(values):
            values[idx] = count
    return hours, values

# get stat by day (weekly)
def get_weekly_stats():
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    week_ago = today - timedelta(days=6)
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT strftime('%w', timestamp) as weekday, COUNT(*) 
            FROM events 
            WHERE timestamp >= ? AND type = 'in'
            GROUP BY weekday
        """, (week_ago,))
        rows = cursor.fetchall()
    weekdays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    values = [0 for _ in weekdays]
    for weekday, count in rows:
        values[int(weekday)] = count
    return weekdays[1:] + [weekdays[0]], values[1:] + [values[0]]
