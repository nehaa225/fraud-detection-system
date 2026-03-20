import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="fraud_detection"
    )

def insert_report(user_id, scam_type, description, link):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO scam_reports (user_id, scam_type, description, link) VALUES (%s,%s,%s,%s)",
        (user_id, scam_type, description, link)
    )
    conn.commit()
    conn.close()

def register_user(username, password, role):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, password, role) VALUES (%s,%s,%s)",
        (username, password, role)
    )
    conn.commit()
    conn.close()

def login_user(username, password):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE username=%s AND password=%s",
        (username, password)
    )
    result = cursor.fetchone()
    conn.close()
    return result
# Fetch all users
def get_all_users():
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, username, role, registration_date FROM users")
    result = cursor.fetchall()
    conn.close()
    return result

# Fetch all reports (optional: filter by user)
def get_all_reports(user_id=None):
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    if user_id:
        cursor.execute("SELECT * FROM scam_reports WHERE user_id=%s", (user_id,))
    else:
        cursor.execute("SELECT * FROM scam_reports")
    result = cursor.fetchall()
    conn.close()
    return result