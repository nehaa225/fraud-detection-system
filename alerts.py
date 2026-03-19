import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

def send_alert(email, message):
    msg = EmailMessage()
    msg["Subject"] = "Fraud Alert"
    msg["From"] = EMAIL_USER
    msg["To"] = email
    msg.set_content(f"Suspicious message:\n{message}")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_USER, EMAIL_PASS)
        smtp.send_message(msg)