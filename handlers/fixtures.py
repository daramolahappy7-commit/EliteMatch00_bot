import datetime
from telegram import Update
from telegram.ext import ContextTypes
from services.sports_api import SportsAPIService

sports_service = SportsAPIService()

async def fixtures_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    fixtures = await sports_service.get_fixtures(today)
    
    if not fixtures:
        await update.effective_message.reply_text("📅 No upcoming fixtures found for today.")
        return

    text = "📅 **UPCOMING FIXTURES TODAY**\n\n"
    for f in fixtures[:8]:
        league = f.get("league", {}).get("name")
        home = f.get("teams", {}).get("home", {}).get("name")
        away = f.get("teams", {}).get("away", {}).get("name")
        time_str = f.get("fixture", {}).get("date", "")[11:16]
        text += f"🏆 **{league}**\n🔵 {home} vs {away}\n🕐 {time_str} UTC\n\n"

    await update.effective_message.reply_text(text, parse_mode="Markdown")
