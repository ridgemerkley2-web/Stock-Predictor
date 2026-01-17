import asyncio
import hashlib
import json
from typing import Any, Dict, Optional

import httpx

from config import Settings
from rate_limiter import TokenBucket, with_retry


class AlpacaClient:
    def __init__(self, settings: Settings):
        self.settings = settings
        self._bucket = TokenBucket(rate_per_minute=200)
        self._client = httpx.AsyncClient(timeout=10.0)

    async def _headers(self) -> Dict[str, str]:
        return {
            "APCA-API-KEY-ID": self.settings.alpaca_api_key,
            "APCA-API-SECRET-KEY": self.settings.alpaca_api_secret,
            "Content-Type": "application/json",
        }

    async def _request(self, method: str, path: str, payload: Optional[dict] = None):
        limit = await self._bucket.acquire()
        if not limit.allowed:
            await asyncio.sleep(limit.wait_time)
        url = f"{self.settings.alpaca_base_url}{path}"
        return await with_retry(
            self._client.request,
            method,
            url,
            headers=await self._headers(),
            json=payload,
        )

    def build_idempotency_key(self, order: Dict[str, Any]) -> str:
        payload = json.dumps(order, sort_keys=True)
        return hashlib.sha256(payload.encode()).hexdigest()

    async def submit_order(self, order: Dict[str, Any]) -> Dict[str, Any]:
        idempotency_key = self.build_idempotency_key(order)
        payload = {**order, "client_order_id": idempotency_key}
        response = await self._request("POST", "/v2/orders", payload)
        response.raise_for_status()
        return response.json()

    async def get_account(self) -> Dict[str, Any]:
        response = await self._request("GET", "/v2/account")
        response.raise_for_status()
        return response.json()

    async def close(self):
        await self._client.aclose()
