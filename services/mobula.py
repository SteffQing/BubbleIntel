
from datatypes.mobula import TokenDataApiRes
from services.httpx import get_client


class Mobula:
    BASE_URL = "https://api.mobula.io/api"
    
    def __init__(self):
        client = get_client()
        self.client = client
        
    
    async def get_token_data(self, asset_address: str):
            response = await self.client.get(f"{self.BASE_URL}/1/market/data", params={"asset": asset_address})
            response.raise_for_status()
            tokenData: TokenDataApiRes = response.json()
            return tokenData['data']