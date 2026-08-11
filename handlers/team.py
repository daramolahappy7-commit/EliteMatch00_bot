from telegram import Update
from telegram.ext import ContextTypes
from services.sports_api import SportsAPIService

sports_service = SportsAPIService()

async def team_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.effective_message.reply_text("🔍 Please provide a team name. Example:\n`/team Arsenal`", parse_mode="Markdown")
        return

    query = " ".join(context.args)
    res = await sports_service.search_team(query)
    if not res:
        await update.effective_message.reply_text(f"⚠️ Team **{query}** not found.", parse_mode="Markdown")
        return

    team = res[0].get("team", {})
    venue = res[0].get("venue", {})

    msg = (
        f"🛡 **TEAM INFO: {team.get('name')}**\n\n"
        f"🏳️ **Country:** {team.get('country')}\n"
        f"📅 **Founded:** {team.get('founded')}\n"
        f"🏟 **Stadium:** {venue.get('name')} ({venue.get('city')})\n"
        f"Capacity: {venue.get('capacity')}"
    )
    await update.effective_message.reply_text(msg, parse_mode="Markdown")
