app.py

from flask import Flask, render_template, request, session, redirect, jsonify
import sqlite3
import os
from logic_similarity import compute_similarity

#----------------- Flask App -----------------

app = Flask(name, template_folder='templates', static_folder='static')
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "default_secret")

#----------------- Auto-create Database Tables -----------------

def init_db():
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    email TEXT UNIQUE,
    password TEXT
)
""")

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

init_db()

#----------------- Database Connection -----------------

def get_db():
conn = sqlite3.connect("database.db")
conn.row_factory = sqlite3.Row
return conn

#----------------- Pages -----------------

@app.route("/")
def index():
return redirect("/hackathon.html")

@app.route("/hackathon.html")
def home():
return render_template("hackathon.html")

@app.route("/hackabout.html")
def about():
return render_template("hackabout.html")

@app.route("/hacklogin.html")
def login():
return render_template("hacklogin.html")

@app.route("/signup.html")
def signup():
return render_template("signup.html")

@app.route("/hackdetection.html")
def detector():
if 'user_id' not in session:
return redirect("/hacklogin.html")
return render_template("hackdetection.html")

@app.route("/hackhistory.html")
def history():
if 'user_id' not in session:
return redirect("/hacklogin.html")

conn = get_db()
cursor = conn.cursor()
cursor.execute(
    "SELECT * FROM reports WHERE user_id=? ORDER BY id DESC",
    (session['user_id'],)
)
reports = cursor.fetchall()
conn.close()

return render_template("hackhistory.html", reports=reports)

#----------------- Signup -----------------

@app.route("/signup_user", methods=["POST"])
def signup_user():

username = request.form.get("username", "").strip()
email = request.form.get("email", "").strip()
password = request.form.get("password", "").strip()

if not username or not email or not password:
    return jsonify({"status": "fail", "message": "All fields are required"})

conn = get_db()
cursor = conn.cursor()

try:
    cursor.execute(
        "INSERT INTO users(username,email,password) VALUES(?,?,?)",
        (username, email, password)
    )

    conn.commit()
    session['user_id'] = cursor.lastrowid
    conn.close()

    return jsonify({"status": "success"})

except sqlite3.IntegrityError:
    conn.close()
    return jsonify({"status": "fail", "message": "Email already exists"})

#----------------- Login -----------------

@app.route("/login_user", methods=["POST"])
def login_user():

email = request.form.get("email", "").strip()
password = request.form.get("password", "").strip()

if not email or not password:
    return jsonify({"status": "fail", "message": "All fields are required"})

conn = get_db()
cursor = conn.cursor()

cursor.execute(
    "SELECT * FROM users WHERE email=? AND password=?",
    (email, password)
)

user = cursor.fetchone()
conn.close()

if user:
    session['user_id'] = user['id']
    return jsonify({"status": "success"})
else:
    return jsonify({"status": "fail", "message": "Invalid credentials"})

#----------------- Plagiarism Detection -----------------

@app.route("/check", methods=["POST"])
def check():

if 'user_id' not in session:
    return jsonify({"error": "not_logged_in"}), 401

code1 = request.form.get("code1", "").strip()
code2 = request.form.get("code2", "").strip()
language = request.form.get("language", "python")

if not code1 or not code2:
    return jsonify({"error": "Please enter code in both fields"}), 400

percent = compute_similarity(code1, code2, language)

if percent <= 30:
    level = "Low Plagiarism"
elif percent <= 70:
    level = "Medium Plagiarism"
else:
    level = "High Plagiarism"

tokens1 = code1.split()
tokens2 = code2.split()

matched_tokens = len(set(tokens1) & set(tokens2))
code1_length = len(tokens1)
code2_length = len(tokens2)

conn = get_db()
cursor = conn.cursor()

cursor.execute(
    "INSERT INTO reports(user_id, similarity, code1, code2, language) VALUES (?, ?, ?, ?, ?)",
    (session['user_id'], percent, code1, code2, language)
)

conn.commit()
conn.close()

return jsonify({
    "similarity": percent,
    "level": level,
    "matched_tokens": matched_tokens,
    "code1_length": code1_length,
    "code2_length": code2_length,
    "language": language
})

#----------------- Logout -----------------

@app.route("/logout")
def logout():
session.pop('user_id', None)
return redirect("/hacklogin.html")

@app.route("/healthz")
def health():
return "OK"

#----------------- Run -----------------

if name == "main":
port = int(os.environ.get("PORT", 10000))
app.run(host="0.0.0.0", port=port)
