import smtplib
from email.message import EmailMessage
from os import getenv

from celery_app import celeryApp


@celeryApp.task
def send_email(email, token):
    msg = EmailMessage()
    msg['Subject'] = "Token Verification"
    msg['From'] = getenv("MAIL_USERNAME")
    msg['To'] = email
    msg.set_content(f"http://127.0.0.1:8000/user/verify_token/{token}")
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(getenv("MAIL_USERNAME"), getenv("MAIL_PASSWORD"))
        smtp.send_message(msg)
    return 'email sent successfully'
