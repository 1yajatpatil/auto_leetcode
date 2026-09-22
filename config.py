import os
from pathlib import Path

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

BASE_DIR = Path(__file__).resolve().parent
STATE_DIR = BASE_DIR / "state"
STATE_DIR.mkdir(exist_ok=True)

LEETCODE_USERNAME = os.environ.get("LEETCODE_USERNAME")
SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
RECIPIENT_EMAIL = os.environ.get("RECIPIENT_EMAIL")

SMTP_APP_PASSWORD = os.environ.get("SMTP_APP_PASSWORD")
SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))

PROBLEM_COUNT = int(os.environ.get("PROBLEM_COUNT", "7"))
EASY_RATIO = float(os.environ.get("EASY_RATIO", "0.4"))  # ~40% easy / 60% medium

SENT_PROBLEMS_FILE = STATE_DIR / "sent_problems.json"
PROBLEMS_TODAY_FILE = STATE_DIR / "problems_today.json"
EMAIL_BODY_FILE = STATE_DIR / "email_body.html"
HISTORY_LOG_FILE = STATE_DIR / "history.log"
