import sqlite3
from datetime import datetime, timedelta

DB_NAME = "db.sqlite3"

def log_event(event_type):
    """
    Записывает событие event_type с текущей меткой времени в таблицу events.
    """
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO events (type, timestamp) VALUES (?, datetime('now'))",
        (event_type,)
    )
    conn.commit()
    conn.close()

def init_db():
    """
    Создаёт таблицу events, если её нет.
    """
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

def add_event(event_type):
    """
    Сохраняет простое событие без метки времени (если нужно).
    """
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO events (type) VALUES (?)", (event_type,))
        conn.commit()

def get_daily_stats():
    """
    Возвращает списки меток часов (6–7 … 21–22) и 
    количества входов в каждый час за сегодня.
    """
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

    hours = [f"{h}–{h+1}" for h in range(6, 22)]
    values = [0] * len(hours)
    for hour_str, count in rows:
        h = int(hour_str)
        idx = h - 6
        if 0 <= idx < len(values):
            values[idx] = count
    return hours, values

def get_weekly_stats():
    """
    Возвращает списки меток дней недели и 
    количества входов за каждый из последних 7 дней.
    """
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

    # strftime('%w'): 0=Sun … 6=Sat
    labels = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    counts = [0] * 7
    for weekday_str, count in rows:
        idx = int(weekday_str)
        counts[idx] = count

    # Переставляем, чтобы неделя шла Mon…Sun
    return labels[1:] + [labels[0]], counts[1:] + [counts[0]]
