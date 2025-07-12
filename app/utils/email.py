import smtplib
from email.message import EmailMessage
from app.config import EMAIL_SENDER, EMAIL_PASSWORD, SMTP_SERVER, SMTP_PORT

if not EMAIL_SENDER or not EMAIL_PASSWORD or not SMTP_SERVER or not SMTP_PORT:
    raise ValueError("Not enough data")

async def send_verification_email(to_email: str, verify_url: str):
    msg = EmailMessage()
    msg['Subject'] = 'Verify your email'
    msg['From'] = EMAIL_SENDER
    msg['To'] = to_email
    msg.set_content(f'Click this link to verify your email: {verify_url}')

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)
