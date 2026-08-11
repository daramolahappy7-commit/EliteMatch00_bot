import logging
import asyncio
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from config import Config
from database.database import init_db
from services.scheduler import setup_scheduler

# Handlers
from handlers.start import start_command
from handlers.help import help_command
from handlers.live import live_command
from handlers.news import news_command
from handlers.fixtures import fixtures_command
from handlers.results import results_command
from handlers.standings import standings_command
from handlers.team import team_command
from handlers.player import player_command
from handlers.insights import insights_command
from handlers.alerts import alerts_command
from handlers.about import about_command
from handlers.callbacks import button_callback_handler

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def main():
    logger.info("Initializing Database...")
    await init_db()

    if not Config.TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN is missing!")
        return

    app = ApplicationBuilder().token(Config.TELEGRAM_BOT_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("live", live_command))
    app.add_handler(CommandHandler("news", news_command))
    app.add_handler(CommandHandler("fixtures", fixtures_command))
    app.add_handler(CommandHandler("results", results_command))
    app.add_handler(CommandHandler("standings", standings_command))
    app.add_handler(CommandHandler("team", team_command))
    app.add_handler(CommandHandler("player", player_command))
    app.add_handler(CommandHandler("insights", insights_command))
    app.add_handler(CommandHandler("alerts", alerts_command))
    app.add_handler(CommandHandler("about", about_command))

    # Callbacks
    app.add_handler(CallbackQueryHandler(button_callback_handler))

    # Scheduler setup for channel posts
    scheduler = setup_scheduler(app)

    logger.info("Starting Bot Polling...")
    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    # Run loop
    try:
        await asyncio.Event().wait()
    finally:
        await app.updater.stop()
        await app.stop()
        scheduler.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
