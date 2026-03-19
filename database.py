import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password",
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