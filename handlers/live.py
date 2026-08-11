from telegram import Update
from telegram.ext import ContextTypes
from services.sports_api import SportsAPIService

sports_service = SportsAPIService()

async def live_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    matches = await sports_service.get_live_matches()
    if not matches:
        text = "⚽ **LIVE MATCHES**\n\nThere are no live matches in monitored leagues right now."
        if update.callback_query:
            await update.callback_query.message.reply_text(text, parse_mode="Markdown")
        else:
            await update.message.reply_text(text, parse_mode="Markdown")
        return

    for match in matches[:5]:
        league = match.get("league", {}).get("name", "Unknown League")
        home = match.get("teams", {}).get("home", {}).get("name")
        away = match.get("teams", {}).get("away", {}).get("name")
        goals_h = match.get("goals", {}).get("home", 0)
        goals_a = match.get("goals", {}).get("away", 0)
        elapsed = match.get("fixture", {}).get("status", {}).get("elapsed", 0)

        msg = (
            "⚽ **LIVE MATCH**\n\n"
            f"🏆 **{league}**\n\n"
            f"🔵 {home} {goals_h} - {goals_a} {away} 🔴\n\n"
            f"⏱ **{elapsed}'**\n\n"
            "🔥 Match is still live!"
        )
        if update.callback_query:
            await update.callback_query.message.reply_text(msg, parse_mode="Markdown")
        else:
            await update.message.reply_text(msg, parse_mode="Markdown")
