import smtplib
from email.mime.text import MIMEText
import os
from typing import List
from fastapi import WebSocket

websocket_connections: List[WebSocket] = []

async def send_websocket_notification(message: str):
    for connection in websocket_connections:
        await connection.send_text(message)

def send_email_notification(message: str, to_email: str = "admin@example.com"):
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")

    if not smtp_server:
        print("SMTP not configured. Logging to console: " + message)
        return

    msg = MIMEText(message)
    msg['Subject'] = 'IT Helpdesk Notification'
    msg['From'] = smtp_user
    msg['To'] = to_email

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_user, to_email, msg.as_string())
    except Exception as e:
        print(f"Email failed: {e}. Logging to console: " + message)

def send_notification(message: str):
    print(message)  
    send_email_notification(message)
    