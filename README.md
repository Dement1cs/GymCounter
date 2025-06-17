# GymCounter

**GymCounter** is a simple IoT system for tracking gym visits based on Raspberry Pi, Flask and SQLite.

## About

- Allows real-time tracking of the number of people in the room via physical and virtual (web buttons)
- Uses two buttons (IN/OUT) on Raspberry Pi to increase/decrease the counter
- Automatic reset of “forgotten to leave” users by timer (60 minutes)
- Web interface shows the current counter and daily/weekly statistics

## Quick start

1. **Clone the repository and go to the folder**
```bash
git clone https://github.com/Dement1cs/GymCounter.git
cd GymCounter
```
2. **Create a virtual environment and install dependencies**
```bash
python -m venv venv
pip install -r requirements.txt
```
3. **Initialize the database**
```bash
python -c "from db import init_db; init_db()"
```
4. **run application**
```bash
python app.py
```

## Dependencies
```bash
pip install Flask
pip install pytest
```
