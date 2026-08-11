from telegram import Update
from telegram.ext import ContextTypes

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    about_text = (
        "ℹ️ **ABOUT EliteMatch00_bot**\n\n"
        "EliteMatch00_bot is an all-in-one sports management platform designed "
        "to deliver real-time scores, news, AI match insights, and channel automation.\n\n"
        "⚡ Powered by Python, Telegram API, Gemini AI, and API-Football."
    )
    await update.effective_message.reply_text(about_text, parse_mode="Markdown")
