from telegram import Update
from telegram.ext import ContextTypes
from services.sports_api import SportsAPIService

sports_service = SportsAPIService()

async def player_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.effective_message.reply_text("🔍 Please provide a player name. Example:\n`/player Haaland`", parse_mode="Markdown")
        return

    query = " ".join(context.args)
    res = await sports_service.search_player(query)
    if not res:
        await update.effective_message.reply_text(f"⚠️ Player **{query}** not found.", parse_mode="Markdown")
        return

    player = res[0].get("player", {})
    msg = (
        f"👤 **PLAYER STATS: {player.get('name')}**\n\n"
        f"🏃 **Position:** {player.get('position')}\n"
        f"🎂 **Age:** {player.get('age')}\n"
        f"🏳️ **Nationality:** {player.get('nationality')}\n"
        f"📏 **Height/Weight:** {player.get('height')} / {player.get('weight')}"
    )
    await update.effective_message.reply_text(msg, parse_mode="Markdown")
