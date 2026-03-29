import httpx
from typing import List, Dict, Any
import os


TRANSACTION_SERVICE_URL = os.getenv("TRANSACTION_SERVICE_URL", "http://localhost:8082")


async def fetch_transactions(token: str) -> List[Dict[str, Any]]:
    url = f"{TRANSACTION_SERVICE_URL}/api/transactions"
    headers = {"Authorization": f"Bearer {token}"}

    # async with httpx.AsyncClient() as client:
    #     response = client.get(url, headers=headers)
    #     response.raise_for_status()
    #     return response.json()

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        return response.json()