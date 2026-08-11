# services/sports_api.py

class SportsAPIService:
    def __init__(self):  # <--- Added 'self' here
        self.headers = {
            "x-apisports-key": Config.SPORTS_API_KEY,
            "x-rapidapi-host": "v3.football.api-sports.io"
        }
        self.base_url = Config.SPORTS_API_BASE_URL
