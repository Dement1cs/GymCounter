from flask import Flask, render_template, redirect, url_for, request
import time
import threading

app = Flask(__name__)
people = []  # сюда будут сохраняться временные метки входов

def auto_remove(ts):
    time.sleep(60 * 60)  # 60 минут
    if ts in people:
        people.remove(ts)
        print("Автовыход сработал")

# Главная страница — описание проекта
@app.route('/')
def index():
    return render_template("index.html")

# Страница активности (счётчик + кнопки)
@app.route('/activity')
def activity():
    return render_template("activity.html", count=len(people))

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

if __name__ == '__main__':
    app.run(debug=True)