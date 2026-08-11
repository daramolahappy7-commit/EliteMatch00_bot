from telegram import Update
from telegram.ext import ContextTypes

async def alerts_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🔔 **MATCH ALERTS MANAGEMENT**\n\n"
        "To subscribe to live match notifications, use:\n"
        "`/alert_add <match_id>`\n\n"
        "To view active notifications:\n"
        "`/alert_list`"
    )
    await update.effective_message.reply_text(text, parse_mode="Markdown")
