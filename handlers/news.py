from telegram import Update
from telegram.ext import ContextTypes
from services.news_api import NewsAPIService

async def news_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    articles = await NewsAPIService.get_latest_sports_news()
    if not articles:
        await update.effective_message.reply_text("⚠️ Unable to fetch sports news at the moment.")
        return

    for article in articles[:3]:
        title = article.get("title", "Sports Update")
        desc = article.get("description", "No summary available.")
        url = article.get("url", "#")
        
        msg = (
            "📰 **LATEST SPORTS NEWS**\n\n"
            f"🔥 **{title}**\n\n"
            f"{desc}\n\n"
            f"🔗 [Read More]({url})"
        )
        await update.effective_message.reply_text(msg, parse_mode="Markdown", disable_web_page_preview=False)
