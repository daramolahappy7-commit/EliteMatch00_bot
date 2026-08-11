from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database.database import AsyncSessionLocal, User

def get_main_menu_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("⚽ Live Matches", callback_data="btn_live"),
            InlineKeyboardButton("📰 Latest News", callback_data="btn_news")
        ],
        [
            InlineKeyboardButton("📅 Fixtures", callback_data="btn_fixtures"),
            InlineKeyboardButton("🏆 Results", callback_data="btn_results")
        ],
        [
            InlineKeyboardButton("📊 Standings", callback_data="btn_standings"),
            InlineKeyboardButton("👤 Player Stats", callback_data="btn_player")
        ],
        [
            InlineKeyboardButton("🤖 AI Insights", callback_data="btn_insights"),
            InlineKeyboardButton("🔔 Match Alerts", callback_data="btn_alerts")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = update.effective_user
    async with AsyncSessionLocal() as session:
        user = await session.get(User, user_data.id)
        if not user:
            user = User(id=user_data.id, username=user_data.username, first_name=user_data.first_name)
            session.add(user)
            await session.commit()

    text = (
        f"👋 Welcome to **EliteMatch00_bot**, {user_data.first_name}!\n\n"
        "Your ultimate sports hub for live scores, news, fixtures, results, standings, and AI insights.\n\n"
        "Select an option from the menu below to get started:"
    )
    if update.message:
        await update.message.reply_text(text, parse_mode="Markdown", reply_markup=get_main_menu_keyboard())
    elif update.callback_query:
        await update.callback_query.message.reply_text(text, parse_mode="Markdown", reply_markup=get_main_menu_keyboard())
