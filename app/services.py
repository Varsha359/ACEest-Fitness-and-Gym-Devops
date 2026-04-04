import sqlite3
from datetime import datetime
import io
import base64
import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt


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


def get_progress_data(name):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT week, adherence
        FROM progress
        WHERE client_name=?
        ORDER BY id
    """, (name,))

    data = cur.fetchall()
    conn.close()
    return data


def generate_chart(name):
    data = get_progress_data(name)

    if not data:
        return None

    weeks = [row[0] for row in data]
    adherence = [row[1] for row in data]

    plt.figure()
    plt.plot(weeks, adherence, marker="o")
    plt.xlabel("Week")
    plt.ylabel("Adherence (%)")
    plt.title(f"Progress - {name}")
    plt.xticks(rotation=45)

    img = io.BytesIO()
    plt.savefig(img, format="png", bbox_inches="tight")
    plt.close()

    img.seek(0)
    return base64.b64encode(img.getvalue()).decode()