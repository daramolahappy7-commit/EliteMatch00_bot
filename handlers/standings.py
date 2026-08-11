from telegram import Update
from telegram.ext import ContextTypes
from services.sports_api import SportsAPIService

sports_service = SportsAPIService()

async def standings_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = await sports_service.get_standings(league_id=39, season=2024)
    if not data or not data[0].get("league", {}).get("standings"):
        await update.effective_message.reply_text("📊 League standings currently unavailable.")
        return

    standings = data[0]["league"]["standings"][0]
    league_name = data[0]["league"]["name"]
    
    text = f"📊 **{league_name} STANDINGS**\n\n"
    text += "`Pos Team            P   W  D  L  PTS`\n"
    for row in standings[:10]:
        pos = str(row['rank']).ljust(3)
        team = row['team']['name'][:12].ljust(13)
        p = str(row['all']['played']).ljust(3)
        pts = str(row['points'])
        text += f"`{pos}{team}{p} {pts}`\n"

    await update.effective_message.reply_text(text, parse_mode="Markdown")
