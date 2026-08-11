from telegram import Update
from telegram.ext import ContextTypes
from services.ai_service import AIService

ai_service = AIService()

async def insights_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    team_a = args[0] if len(args) > 0 else "Manchester City"
    team_b = args[1] if len(args) > 1 else "Arsenal"

    insight = await ai_service.generate_match_insight(team_a, team_b)
    await update.effective_message.reply_text(insight, parse_mode="Markdown")
