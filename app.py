from flask import Flask, render_template, redirect, url_for, request
from db import init_db, add_event, get_daily_stats, get_weekly_stats
import time
import threading

app = Flask(__name__)
people = []  #временные метки входов

def auto_remove(ts):
    time.sleep(60 * 60)  #60 мин
    if ts in people:
        people.remove(ts)
        print("Автовыход сработал")

# Главная страница | main page
@app.route('/')
def index():
    return render_template("index.html")

# Страница активности | activity page
@app.route('/activity')
def activity():
    return render_template("activity.html", count=len(people))

#FAKE STAT
"""
# Обработка входа (IN)
@app.route('/in', methods=['POST'])
def mark_in():
    ts = time.time()
    people.append(ts)
    threading.Thread(target=auto_remove, args=(ts,), daemon=True).start()
    return redirect(url_for('activity'))

# Обработка выхода (OUT)
@app.route('/out', methods=['POST'])
def mark_out():
    if people:
        people.pop(0)
    return redirect(url_for('activity'))

@app.route('/api/daily')
def api_daily():
    labels = ["6–7", "7–8", "8–9", "9–10", "10–11", "11–12", "12–13", "13–14",
              "14–15", "15–16", "16–17", "17–18", "18–19", "19–20", "20–21", "21–22"]
    values = [12, 18, 25, 30, 28, 22, 20, 17, 15, 18, 24, 40, 55, 60, 45, 20]
    return { "labels": labels, "values": values }
    
@app.route('/api/weekly')
def api_weekly():
    labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    values = [120, 135, 150, 140, 160, 200, 180]
    return { "labels": labels, "values": values }
"""

#TRUE STAT
init_db()

@app.route('/in', methods=['POST'])
def mark_in():
    ts = time.time()
    people.append(ts)
    add_event("in")
    threading.Thread(target=auto_remove, args=(ts,), daemon=True).start()
    return redirect(url_for('activity'))

@app.route('/out', methods=['POST'])
def mark_out():
    if people:
        people.pop(0)
    add_event("out")
    return redirect(url_for('activity'))

@app.route('/api/daily')
def api_daily():
    labels, values = get_daily_stats()
    return {"labels": labels, "values": values}

@app.route('/api/weekly')
def api_weekly():
    labels, values = get_weekly_stats()
    return {"labels": labels, "values": values}

@app.route('/api/count')
def api_count():
    return {"count": len(people)}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)