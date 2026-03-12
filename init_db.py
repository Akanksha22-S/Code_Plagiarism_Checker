import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# ================= USERS TABLE =================
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    email TEXT UNIQUE,
    password TEXT
)
""")

# ================= REPORTS TABLE =================
cursor.execute("""
CREATE TABLE IF NOT EXISTS reports(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    similarity REAL,
    code1 TEXT,
    code2 TEXT,
    language TEXT
)
""")

conn.commit()
conn.close()
print("Database created successfully")
