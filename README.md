# Stock Predictor - Alpaca Algo Trading Monorepo

Production-style, research-first algo trading system that scans the US equity market, generates signals, and executes via Alpaca (paper default) with strict risk controls and blind backtesting.

## Repository layout
```
apps/
  api/        FastAPI REST + WebSocket API
  worker/     Async workers (scanner, signals, risk, executor, research)
  web/        Next.js App Router UI
 tests/       Unit tests for research + execution safety
```

## Quick start
1. Copy environment settings.
   ```bash
   cp .env.example .env
   ```
2. Start Postgres/Redis.
   ```bash
   docker-compose up -d
   ```
3. Install API deps and run.
   ```bash
   cd apps/api
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```
4. Run a worker (paper by default).
   ```bash
   cd apps/worker
   python -m cli run-live
   ```
5. Start the web app (optional).
   ```bash
   cd apps/web
   npm install
   npm run dev
   ```

## Deployment
This repo is intentionally a monorepo so you can deploy each service separately.

### 1) Provision data services
Use any managed Postgres + Redis (or the included docker-compose for dev). Ensure the `POSTGRES_URL` and `REDIS_URL` environment variables point to your production services.

### 2) API (FastAPI)
Run the API behind a process manager (systemd, supervisord) or container platform.
Example (container/VM):
```bash
cd apps/api
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```
Expose port 8000 behind a reverse proxy (NGINX/ALB) and set environment variables from `.env.example`.

### 3) Worker services
Run workers as separate processes/containers (scanner, signals, risk, executor, research).
Example single worker process:
```bash
cd apps/worker
python -m cli run-live
```
Scale horizontally by running multiple worker instances with distinct roles (recommended for scanner vs executor).

### 4) Web app (Next.js)
Build and serve the Next.js app with a static host or Node server:
```bash
cd apps/web
npm install
npm run build
npm run start
```
Point the web UI to the API base URL via environment variables (add a `NEXT_PUBLIC_API_BASE_URL` when you wire the frontend to live data).

### 5) Live trading guardrails
Set `ENABLE_LIVE_TRADING=true` **and** a secure `ADMIN_SECRET` only after validating a bundle via the research workflow and promotion gates.

## Safety rails (paper vs live)
- Paper trading is the default (`ENABLE_LIVE_TRADING=false`).
- Live trading requires `ENABLE_LIVE_TRADING=true` **and** a valid `ADMIN_SECRET`.
- The executor enforces max positions, exposure, daily loss, and drawdown limits before placing orders.
- Kill switch: `flatten_all()` will exit positions immediately.

## Research workflow (blind backtesting)
1. **Ingest data** (for universe or research).
2. **Feature generation** with strict no-lookahead shifts.
3. **Walk-forward optimization** on TRAIN+VAL splits.
4. **Holdout evaluation** once (never used for tuning).
5. **Bundle creation** with parameters, calibration, and metadata.
6. **Promotion gates** before enabling live use.

The research pipeline intentionally enforces time-based splits with optional purge/embargo to prevent leakage.

## CLI commands
From `apps/worker`:
```bash
python -m cli ingest
python -m cli research
python -m cli run-live
python -m cli promote --bundle-id <id>
python -m cli select-bundle --bundle-id <id>
```

## Health checks
- `GET /health` includes Alpaca connectivity checks.
- `GET /health/alpaca` returns stream/auth status details.

## Web UI pages
- **Best Buys Now**: live candidates via WebSocket.
- **Pick detail**: certainty, EV, entry/stop/target.
- **Positions / Orders / Fills**: streaming updates.
- **Risk panel**: exposure, drawdown, circuit breakers.
- **Research**: latest bundles and holdout results.

## Blind backtest definition
“Blind backtest” here means that the final holdout set is never used during tuning or parameter selection. The holdout is evaluated once after walk-forward optimization and saved to the bundle as immutable evidence of out-of-sample behavior.
