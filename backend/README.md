# SarfAI Backend V2

FastAPI + SQLite backend for the SarfAI loan & deposit advisor.

## Quick Start

```bash
cd backend

# 1. Create virtualenv
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env — change SECRET_KEY at minimum

# 4. Run migrations
alembic upgrade head

# 5. Seed database (bank products + admin user)
python seed.py

# 6. Start server
uvicorn app.main:app --reload --port 8000
```

API docs available at: http://localhost:8000/docs

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `SECRET_KEY` | `dev-secret-key-...` | JWT signing key — **change in production** |
| `ALGORITHM` | `HS256` | JWT algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `10080` | 7 days |
| `DATABASE_URL` | `sqlite:///./sarfai.db` | SQLite or PostgreSQL URL |
| `ALLOWED_ORIGINS` | `http://localhost:5173,...` | CORS origins (comma-separated) |
| `ADMIN_USERNAME` | `admin` | Initial admin username |
| `ADMIN_PASSWORD` | `sarfai-admin-2025` | Initial admin password |

## Switching to PostgreSQL

1. Install: `pip install psycopg2-binary`
2. Set in `.env`: `DATABASE_URL=postgresql://user:pass@host:5432/sarfai`
3. Remove `connect_args` block in `app/database.py`
4. Run: `alembic upgrade head && python seed.py`

## ML Model

The ML model must be trained before starting the server:

```bash
cd ml
python train.py --data ../data/sarfai_datasets.xlsx --out .
```

This generates `model.pkl` and `scaler.pkl` which the `/predict` endpoint loads.

## API Endpoints

### Public
- `POST /auth/register` — create account
- `POST /auth/login` — get token
- `GET /banks` — list all active bank products
- `GET /health` — health check

### Authenticated (Bearer token)
- `GET /profile` — get saved profile
- `POST /profile` — create profile
- `PUT /profile` — update profile
- `POST /predict` — ML scoring + per-bank results
- `POST /simulate` — loan cashflow simulation
- `POST /deposit/match` — deposit product matching

### Admin only
- `GET /admin/stats` — platform statistics
- `GET /admin/trends` — approval rate over time
- `GET /admin/purposes` — popular loan purposes
- `GET /admin/banks/popular` — most matched banks
- `GET /admin/programs` — special program trigger counts
- `GET /admin/users` — user list
- `GET /admin/banks` — all bank products
- `PUT /admin/banks/{id}` — edit rates / toggle active

## Docker

```bash
docker build -t sarfai-backend .
docker run -p 8000:8000 -v $(pwd)/data:/app/data sarfai-backend
```
