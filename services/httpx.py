# http_client.py
import httpx

client: httpx.AsyncClient | None = None

def get_client() -> httpx.AsyncClient:
    if client is None:
        raise RuntimeError("HTTP client not initialized")
    return client

async def init_client():
    global client
    client = httpx.AsyncClient()

async def close_client():
    global client
    if client:
        await client.aclose()
        client = None
