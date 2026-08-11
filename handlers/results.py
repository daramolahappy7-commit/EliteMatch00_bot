from telegram import Update
from telegram.ext import ContextTypes
from services.sports_api import SportsAPIService

sports_service = SportsAPIService()

async def results_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    results = await sports_service.get_results(limit=8)
    if not results:
        await update.effective_message.reply_text("🏆 No recent match results found.")
        return

    text = "🏆 **MATCH RESULTS**\n\n"
    for r in results:
        league = r.get("league", {}).get("name")
        home = r.get("teams", {}).get("home", {}).get("name")
        away = r.get("teams", {}).get("away", {}).get("name")
        goals_h = r.get("goals", {}).get("home", 0)
        goals_a = r.get("goals", {}).get("away", 0)
        text += f"⚽ **{league}**\n{home} {goals_h} - {goals_a} {away}\n\n"

    await update.effective_message.reply_text(text, parse_mode="Markdown")
