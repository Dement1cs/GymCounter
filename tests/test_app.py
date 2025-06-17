import pytest
from app import app, people
import sqlite3
import db
from db import init_db

@pytest.fixture(autouse=True)
def client(tmp_path, monkeypatch):
    # Временная БД в tmp_path / Temporary DB in tmp_path
    test_db = tmp_path / "test.sqlite3"
    monkeypatch.setattr(db, "DB_NAME", str(test_db))
    init_db()

    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

#тест для маршрута /in (UC-1, Normal Flow) / test for route /in (UC-1, Normal Flow)
def test_mark_in_increments_counter_and_logs_event(client):
    # список пуст / the list is empty
    people.clear()
    # POST на /in
    response = client.post("/in", follow_redirects=True)
    # Проверка, что статус 200 OK / Checking that the status is 200 OK
    assert response.status_code == 200
    # Проверка, что people увеличился на 1 / Checking that people has increased by 1
    assert len(people) == 1

    # Проверка, что в таблице events появилась запись type='in' / Checking that the events table has a record with type='in'
    conn = sqlite3.connect(db.DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM events WHERE type='in'")
    count_in = cur.fetchone()[0]
    conn.close()

    assert count_in == 1


#Normal Flow тест для /out (UC-2 Normal Flow) / Normal Flow test for /out (UC-2 Normal Flow)
def test_mark_out_decrements_counter_and_logs_event(client):
    # добавить одну метку входа / add one entry label
    people.clear()
    client.post("/in", follow_redirects=True)
    assert len(people) == 1

    # Выход / Exit
    response = client.post("/out", follow_redirects=True)
    assert response.status_code == 200

    # Список people должен стать пустым / The people list should become empty
    assert len(people) == 0

    # В БД должна быть запись 'out' / There should be an 'out' entry in the DB
    conn = sqlite3.connect(db.DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM events WHERE type='out'")
    count_out = cur.fetchone()[0]
    conn.close()
    assert count_out == 1

#OUT при пустом списке (Тест альтернативного потока) / OUT on empty list (Alternate Stream Test)
def test_mark_out_when_empty_logs_event_but_does_not_crash(client):
    # список пуст / the list is empty
    people.clear()
    # Попытка выхода без входа / Attempt to exit without logging in
    response = client.post("/out", follow_redirects=True)
    assert response.status_code == 200
    # people остаётся пустым / people remains empty
    assert len(people) == 0

    # В БД всё равно должна быть запись 'out' / There should still be an 'out' entry in the DB
    conn = sqlite3.connect(db.DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM events WHERE type='out'")
    count_out = cur.fetchone()[0]
    conn.close()
    assert count_out == 1

#Тест страницы /activity (UC-4) / /activity page test (UC-4)
def test_activity_page_shows_current_count(client):
    people.clear()
    # два входа / two entrances
    client.post("/in")
    client.post("/in")
    # Получаем страницу активности / Get the activity page
    response = client.get("/activity")
    assert response.status_code == 200
    # Проверяем, что в HTML есть число "2" / Check if HTML contains the number "2"
    assert b"2" in response.data


#Тест ошибочного маршрута (UC-3 Exceptional Flow) / UC-3 Exceptional Flow Test
def test_invalid_route_returns_404(client):
    response = client.post("/invalid_path")
    assert response.status_code == 404

