from telegram import Update
from telegram.ext import ContextTypes

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "📖 **EliteMatch00_bot Commands Guide**\n\n"
        "/start - Launch main menu\n"
        "/help - Display help menu\n"
        "/live - Currently active matches\n"
        "/news - Top sports headlines\n"
        "/fixtures - Upcoming matches\n"
        "/results - Recent match scores\n"
        "/standings - League rankings\n"
        "/team <name> - Search team information\n"
        "/player <name> - Search player stats\n"
        "/insights - AI-powered match analysis\n"
        "/alerts - Manage notifications\n"
        "/about - Information about EliteMatch00_bot"
    )
    await update.effective_message.reply_text(help_text, parse_mode="Markdown")
