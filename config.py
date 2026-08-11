import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    SPORTS_API_KEY = os.getenv("SPORTS_API_KEY")
    SPORTS_API_BASE_URL = os.getenv("SPORTS_API_BASE_URL", "https://v3.football.api-sports.io")
    NEWS_API_KEY = os.getenv("NEWS_API_KEY")
    NEWS_API_BASE_URL = os.getenv("NEWS_API_BASE_URL", "https://newsapi.org/v2")
    AI_API_KEY = os.getenv("AI_API_KEY")
    CHANNEL_ID = os.getenv("CHANNEL_ID")
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///bot.db")
    
    # Handle Railway dynamic postgresql:// scheme
    if DATABASE_URL and DATABASE_URL.startswith("postgresql://"):
        DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

    UPDATE_1_TIME = os.getenv("UPDATE_1_TIME", "08:00")
    UPDATE_2_TIME = os.getenv("UPDATE_2_TIME", "14:00")
    UPDATE_3_TIME = os.getenv("UPDATE_3_TIME", "20:00")
    TIMEZONE = os.getenv("TIMEZONE", "Africa/Lagos")
