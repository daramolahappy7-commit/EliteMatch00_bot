import logging
import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import timezone
from config import Config
from services.sports_api import SportsAPIService
from services.news_api import NewsAPIService
from services.ai_service import AIService
from database.database import is_content_published, mark_content_published

logger = logging.getLogger(__name__)
sports_service = SportsAPIService()
ai_service = AIService()

def parse_time(time_str: str):
    parts = time_str.split(":")
    return int(parts[0]), int(parts[1])

async def publish_morning_update(app):
    if not Config.CHANNEL_ID:
        return
    news = await NewsAPIService.get_latest_sports_news()
    news_text = ""
    count = 1
    for article in news[:4]:
        title = article.get("title", "Sports News Update")
        news_text += f"{count}️⃣ {title}\n"
        count += 1
    
    if not news_text:
        news_text = "1️⃣ Upcoming major league fixtures scheduled for today.\n2️⃣ Teams preparing for crucial weekend matches."

    msg = (
        "🌅 **GOOD MORNING SPORTS UPDATE**\n\n"
        "📰 **Top Sports News**\n\n"
        f"{news_text}\n"
        "🔥 Stay updated with @EliteMatch00_bot!"
    )
    await app.bot.send_message(chat_id=Config.CHANNEL_ID, text=msg, parse_mode="Markdown")

async def publish_fixture_update(app):
    if not Config.CHANNEL_ID:
        return
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    fixtures = await sports_service.get_fixtures(today)
    
    text = "⚽ **TODAY'S MATCHES**\n\n"
    if fixtures:
        for f in fixtures[:5]:
            league = f.get("league", {}).get("name", "Football")
            home = f.get("teams", {}).get("home", {}).get("name")
            away = f.get("teams", {}).get("away", {}).get("name")
            text += f"🏆 **{league}**\n🔵 {home} vs {away}\n\n"
    else:
        text += "No major fixtures scheduled for today.\n\n"
        
    text += "🔥 Don't miss today's biggest matches!"
    await app.bot.send_message(chat_id=Config.CHANNEL_ID, text=text, parse_mode="Markdown")

async def publish_evening_recap(app):
    if not Config.CHANNEL_ID:
        return
    results = await sports_service.get_results(limit=3)
    res_text = ""
    for r in results:
        home = r.get("teams", {}).get("home", {}).get("name")
        away = r.get("teams", {}).get("away", {}).get("name")
        goals_h = r.get("goals", {}).get("home", 0)
        goals_a = r.get("goals", {}).get("away", 0)
        res_text += f"{home} {goals_h} - {goals_a} {away}\n"

    if not res_text:
        res_text = "Matches completed across major leagues."

    ai_insight = await ai_service.generate_match_insight("Premier League Teams", "Match Day", "Daily Summary")

    msg = (
        "🌙 **DAILY SPORTS RECAP**\n\n"
        "⚽ **Today's Results**\n"
        f"{res_text}\n"
        f"{ai_insight}\n"
    )
    await app.bot.send_message(chat_id=Config.CHANNEL_ID, text=msg, parse_mode="Markdown")

async def check_breaking_news(app):
    if not Config.CHANNEL_ID:
        return
    articles = await NewsAPIService.get_latest_sports_news()
    for article in articles[:2]:
        url = article.get("url")
        if url and not await is_content_published(url):
            await mark_content_published("news", url)
            msg = (
                "📰 **BREAKING SPORTS NEWS**\n\n"
                f"🔥 **{article.get('title')}**\n\n"
                f"{article.get('description', '')}\n\n"
                f"🔗 [Read More]({url})"
            )
            await app.bot.send_message(chat_id=Config.CHANNEL_ID, text=msg, parse_mode="Markdown", disable_web_page_preview=False)
            break

def setup_scheduler(app):
    tz = timezone(Config.TIMEZONE)
    scheduler = AsyncIOScheduler(timezone=tz)

    h1, m1 = parse_time(Config.UPDATE_1_TIME)
    h2, m2 = parse_time(Config.UPDATE_2_TIME)
    h3, m3 = parse_time(Config.UPDATE_3_TIME)

    scheduler.add_job(publish_morning_update, "cron", hour=h1, minute=m1, args=[app])
    scheduler.add_job(publish_fixture_update, "cron", hour=h2, minute=m2, args=[app])
    scheduler.add_job(publish_evening_recap, "cron", hour=h3, minute=m3, args=[app])
    
    # Check for breaking news every 15 minutes
    scheduler.add_job(check_breaking_news, "interval", minutes=15, args=[app])

    scheduler.start()
    return scheduler
