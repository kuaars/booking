import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
    SERVICES = [s.strip() for s in os.getenv("SERVICES", "").split(",") if s.strip()]
    SLOTS = [s.strip() for s in os.getenv("SLOTS", "").split(",") if s.strip()]
    ALLOW_MULTIPLE_BOOKINGS = os.getenv("ALLOW_MULTIPLE_BOOKINGS", "False").strip().lower() == "true"
    ABOUT_TEXT = os.getenv("ABOUT_TEXT", "")
    DAYS_AHEAD = 7
