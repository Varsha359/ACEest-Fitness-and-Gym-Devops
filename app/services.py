import sqlite3
from datetime import datetime

DB_NAME = "aceest.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            age INTEGER,
            weight REAL,
            program TEXT,
            calories INTEGER
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_name TEXT,
            week TEXT,
            adherence INTEGER
        )
    """)

    conn.commit()
    conn.close()


def calculate_calories(weight, factor):
    return int(weight * factor)


def save_client(name, age, weight, program, calories):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT OR REPLACE INTO clients
        (name, age, weight, program, calories)
        VALUES (?, ?, ?, ?, ?)
    """, (name, age, weight, program, calories))

    conn.commit()
    conn.close()


def get_client(name):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM clients WHERE name=?", (name,))
    result = cur.fetchone()

    conn.close()
    return result


def save_progress(name, adherence):
    conn = get_connection()
    cur = conn.cursor()

    week = datetime.now().strftime("Week %U - %Y")

    cur.execute("""
        INSERT INTO progress (client_name, week, adherence)
        VALUES (?, ?, ?)
    """, (name, week, adherence))

    conn.commit()
    conn.close()