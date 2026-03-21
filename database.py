import sqlite3

def connect_db():
    return sqlite3.connect("fraud.db", check_same_thread=False)

# ---------- REGISTER ----------
def register_user(username, password, role):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT, role TEXT)")
    cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
    conn.commit()
    conn.close()

# ---------- LOGIN ----------
def login_user(username, password):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    result = cursor.fetchone()
    conn.close()
    return result

# ---------- GET USERS ----------
def get_all_users():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    data = cursor.fetchall()
    conn.close()
    return [{"id":i[0], "username":i[1], "password":i[2], "role":i[3]} for i in data]

# ---------- REPORT ----------
def insert_report(user_id, typ, desc, link):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS reports (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, type TEXT, description TEXT, link TEXT)")
    cursor.execute("INSERT INTO reports (user_id, type, description, link) VALUES (?, ?, ?, ?)", (user_id, typ, desc, link))
    conn.commit()
    conn.close()

def get_all_reports():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reports")
    data = cursor.fetchall()
    conn.close()
    return [{"id":i[0], "user_id":i[1], "type":i[2], "description":i[3], "link":i[4]} for i in data]