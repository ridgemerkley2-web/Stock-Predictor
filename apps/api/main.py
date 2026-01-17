import os
from datetime import datetime

import httpx
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from schemas import Bundle, Candidate, Order, Position, RiskState

app = FastAPI(title="Stock Predictor API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "timestamp": datetime.utcnow(),
        "alpaca": await alpaca_health(),
    }


@app.get("/health/alpaca")
async def alpaca_health():
    base_url = os.getenv("ALPACA_BASE_URL", "https://paper-api.alpaca.markets")
    api_key = os.getenv("ALPACA_API_KEY")
    api_secret = os.getenv("ALPACA_API_SECRET")
    if not api_key or not api_secret:
        return {"status": "missing_keys"}

    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            resp = await client.get(
                f"{base_url}/v2/account",
                headers={
                    "APCA-API-KEY-ID": api_key,
                    "APCA-API-SECRET-KEY": api_secret,
                },
            )
            return {"status": "ok" if resp.status_code == 200 else "error", "code": resp.status_code}
        except httpx.RequestError:
            return {"status": "unreachable"}


@app.get("/candidates", response_model=list[Candidate])
async def list_candidates():
    return []


@app.get("/positions", response_model=list[Position])
async def list_positions():
    return []


@app.get("/orders", response_model=list[Order])
async def list_orders():
    return []


@app.get("/risk", response_model=RiskState)
async def risk_state():
    return RiskState(
        equity=0,
        gross_exposure=0,
        max_positions=10,
        daily_loss_limit=0.03,
        drawdown_limit=0.1,
        circuit_breaker_tripped=False,
    )


@app.get("/bundles", response_model=list[Bundle])
async def list_bundles():
    return []


@app.websocket("/ws/candidates")
async def ws_candidates(socket: WebSocket):
    await socket.accept()
    await socket.send_json({"type": "snapshot", "data": []})
    await socket.close()


@app.websocket("/ws/positions")
async def ws_positions(socket: WebSocket):
    await socket.accept()
    await socket.send_json({"type": "snapshot", "data": []})
    await socket.close()
