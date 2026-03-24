import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_alert(receiver_email, scam_content):
    """
    Sends an email alert when fraud is detected.
    """
    # --- Configuration ---
    sender_email = "your_email@gmail.com" 
    sender_password = "your_app_password" # Use an App Password, not your real password
    
    subject = "🚨 Guardian AI: Fraudulent Activity Detected"
    body = f"""
    The Guardian AI system has flagged a message as FRAUD.
    
    Detected Content:
    -----------------
    {scam_content}
    -----------------
    
    Please do not click any links or provide personal information.
    """

    # --- Create Message ---
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Using Gmail's SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False