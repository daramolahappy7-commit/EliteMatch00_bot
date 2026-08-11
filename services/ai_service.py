import logging
from google import genai
from config import Config

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        if Config.AI_API_KEY:
            self.client = genai.Client(api_key=Config.AI_API_KEY)
        else:
            self.client = None

    async def generate_match_insight(self, team_a: str, team_b: str, context: str = "") -> str:
        if not self.client:
            return "🤖 **AI Insight**\n\nAnalysis unavailable. Gemini API key missing."
        
        prompt = (
            f"Provide a neutral, high-level sports analysis for a match between {team_a} and {team_b}.\n"
            f"Context: {context}\n"
            f"Keep it concise, well-formatted with emojis, and end with the explicit disclaimer:\n"
            f"'⚠️ This is AI-generated analysis and is not a guaranteed prediction.'"
        )
        
        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )
            return response.text
        except Exception as e:
            logger.error(f"Gemini API Error: {e}")
            return "⚠️ Unable to generate AI match insights at this moment."
