import httpx
import logging
from config import Config

logger = logging.getLogger(__name__)

class NewsAPIService:
    @staticmethod
    async def get_latest_sports_news():
        if not Config.NEWS_API_KEY:
            return []
        url = f"{Config.NEWS_API_BASE_URL}/top-headlines"
        params = {
            "category": "sports",
            "language": "en",
            "pageSize": 10,
            "apiKey": Config.NEWS_API_KEY
        }
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.get(url, params=params)
                if res.status_code == 200:
                    return res.json().get("articles", [])
                return []
        except Exception as e:
            logger.error(f"News API Exception: {e}")
            return []
