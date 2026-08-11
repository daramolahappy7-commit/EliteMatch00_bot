import httpx
import logging
from config import Config

logger = logging.getLogger(__name__)

class SportsAPIService:
    def __init__():
        self.headers = {
            "x-apisports-key": Config.SPORTS_API_KEY,
            "x-rapidapi-host": "v3.football.api-sports.io"
        }
        self.base_url = Config.SPORTS_API_BASE_URL

    async def _get(self, endpoint: str, params: dict = None):
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.get(f"{self.base_url}/{endpoint}", headers=self.headers, params=params)
                if res.status_code == 200:
                    return res.json().get("response", [])
                logger.error(f"API Error {res.status_code}: {res.text}")
                return []
        except Exception as e:
            logger.error(f"Sports API Request Exception: {e}")
            return []

    async def get_live_matches(self):
        return await self._get("fixtures", {"live": "all"})

    async def get_fixtures(self, date_str: str):
        return await self._get("fixtures", {"date": date_str})

    async def get_results(self, limit: int = 10):
        data = await self._get("fixtures", {"last": limit})
        return data

    async def get_standings(self, league_id: int = 39, season: int = 2024):
        return await self._get("standings", {"league": league_id, "season": season})

    async def search_team(self, team_name: str):
        return await self._get("teams", {"search": team_name})

    async def search_player(self, player_name: str):
        return await self._get("players/profiles", {"search": player_name})
