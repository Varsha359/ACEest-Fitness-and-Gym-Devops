import sqlite3
from datetime import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io, base64
from fpdf import FPDF
import os

DB_NAME = "aceest.db"

def get_conn():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT, role TEXT)")
    cur.execute("""CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        age INTEGER,
        weight REAL,
        program TEXT,
        calories INTEGER,
        membership_status TEXT
    )""")

    cur.execute("CREATE TABLE IF NOT EXISTS progress (id INTEGER PRIMARY KEY, client_name TEXT, week TEXT, adherence INTEGER)")

    cur.execute("SELECT * FROM users WHERE username='admin'")
    if not cur.fetchone():
        cur.execute("INSERT INTO users VALUES ('admin','admin','Admin')")

    conn.commit()
    conn.close()

def validate_user(u, p):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT role FROM users WHERE username=? AND password=?", (u,p))
    row = cur.fetchone()
    conn.close()
    return row

def save_client(name):
    if not name:
        return
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO clients (name, membership_status) VALUES (?,?)",(name,"Active"))
    conn.commit()
    conn.close()

def get_clients():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT name FROM clients")
    data = [r[0] for r in cur.fetchall()]
    conn.close()
    return data

def save_progress(name, adherence):
    if not name:
        return
    conn = get_conn()
    cur = conn.cursor()
    week = datetime.now().strftime("Week %U - %Y")
    cur.execute("INSERT INTO progress (client_name, week, adherence) VALUES (?,?,?)",(name,week,adherence))
    conn.commit()
    conn.close()

def get_progress(name):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT week, adherence FROM progress WHERE client_name=?",(name,))
    data = cur.fetchall()
    conn.close()
    return data

def generate_chart(name):
    data = get_progress(name)
    if not data:
        return None

    weeks = [d[0] for d in data]
    vals = [d[1] for d in data]

    plt.figure()
    plt.plot(weeks, vals, marker="o")
    plt.xticks(rotation=45)

    img = io.BytesIO()
    plt.savefig(img, format="png")
    plt.close()

    return base64.b64encode(img.getvalue()).decode()

def generate_pdf(name):
    # ✅ Fix 1: handle empty name
    if not name:
        name = "fitness_report"

    # ✅ Fix 2: absolute path
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(BASE_DIR, f"{name}.pdf")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial","B",16)
    pdf.cell(0,10,f"ACEest Report - {name}",ln=True)

    pdf.output(filepath)

    return filepath