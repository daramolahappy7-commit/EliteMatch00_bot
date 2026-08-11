import logging
from telegram.ext import Application
from database.database import AsyncSessionLocal, MatchAlert
from sqlalchemy import select

logger = logging.getLogger(__name__)

async def notify_match_event(app: Application, match_id: int, event_text: str):
    async with AsyncSessionLocal() as session:
        stmt = select(MatchAlert).where(MatchAlert.match_id == match_id)
        result = await session.execute(stmt)
        alerts = result.scalars().all()
        
        for alert in alerts:
            try:
                await app.bot.send_message(
                    chat_id=alert.user_id,
                    text=f"🔔 **MATCH ALERT**\n\n{event_text}",
                    parse_mode="Markdown"
                )
            except Exception as e:
                logger.error(f"Failed to send alert to {alert.user_id}: {e}")
