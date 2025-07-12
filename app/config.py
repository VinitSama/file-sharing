import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")