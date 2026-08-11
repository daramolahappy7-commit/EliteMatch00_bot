from telegram import Update
from telegram.ext import ContextTypes
from handlers.live import live_command
from handlers.news import news_command
from handlers.fixtures import fixtures_command
from handlers.results import results_command
from handlers.standings import standings_command
from handlers.player import player_command
from handlers.insights import insights_command
from handlers.alerts import alerts_command

async def button_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    if data == "btn_live":
        await live_command(update, context)
    elif data == "btn_news":
        await news_command(update, context)
    elif data == "btn_fixtures":
        await fixtures_command(update, context)
    elif data == "btn_results":
        await results_command(update, context)
    elif data == "btn_standings":
        await standings_command(update, context)
    elif data == "btn_player":
        await query.message.reply_text("🔍 Search player stats using command: `/player <name>`", parse_mode="Markdown")
    elif data == "btn_insights":
        await insights_command(update, context)
    elif data == "btn_alerts":
        await alerts_command(update, context)
