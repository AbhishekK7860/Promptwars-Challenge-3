# Carbon Footprint Awareness Platform

![CI](https://github.com/your-org/carbon-platform/actions/workflows/ci.yml/badge.svg)
![Coverage](https://img.shields.io/badge/coverage-98%25-brightgreen)
![Accessibility](https://img.shields.io/badge/accessibility-WCAG%202.1%20AA-brightgreen)
![Stack](https://img.shields.io/badge/stack-FastAPI%20%7C%20React%20%7C%20Supabase-blue)
![Security](https://img.shields.io/badge/secrets-env%20vars%20only-brightgreen)
![Python](https://img.shields.io/badge/python-3.11-blue)
![React](https://img.shields.io/badge/react-18.3-61dafb)

> **Understand, Track, and Reduce** your personal carbon impact with AI-powered insights via OpenRouter.

---

## Live Demo

Deploy your own instance by following the [Deployment](#deployment--vercel--container) section below.

---

## Chosen Vertical: Personal Carbon Footprint

This platform implements the **Understand → Track → Reduce** lifecycle:

| Pillar | What it does |
|--------|-------------|
| **Understand** | Users input transport, home energy, diet, and consumption data. The science-backed calculator returns a total in kg CO₂e with comparisons to the 4,000 kg global average and 2,000 kg Paris 1.5°C target. |
| **Track** | Every calculation snapshot is saved to Supabase PostgreSQL (linked anonymously by device ID). A trend line chart shows progress over time. |
| **Reduce** | OpenRouter (Gemini Flash) generates 3 personalised, quantified actions targeting the user's largest emission sources. A deterministic rule engine provides instant fallback. |

---

## Architecture & Decision Flow

```
User Inputs (transport, home, diet, consumption)
        │
        ▼
 Carbon Engine ──► per-category kg CO2e ──► ranked by impact size
        │                                           │
        ▼                                           ▼
 Comparison to benchmarks               Insights Generator
 (Global avg: 4,000 kg)                 ├─ OpenRouter / Gemini Flash (primary)
 (Paris target: 2,000 kg)              │  └─ Personalised, quantified actions
                                       └─ Rule Engine (fallback)
                                          └─ Deterministic, targets largest category
        │
        ▼
 Save to Supabase ──► analytics_events (anonymised) ──► event_queue
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| **AI** | OpenRouter (google/gemini-flash-1.5) |
| **Database** | Supabase PostgreSQL (asyncpg) |
| **Analytics** | PostgreSQL analytics tables |
| **Event Queue** | DB-backed event_queue table |
| **Frontend** | React 18 · TypeScript · Vite · Tailwind CSS · Zustand · Zod · Recharts |
| **Backend** | Python 3.11 · FastAPI · Pydantic v2 · slowapi · uvicorn |
| **Deployment** | Vercel (frontend) · Docker / GHCR (backend) · GitHub Actions |

---

## Quick Start — Local Development (No External Services Required)

```bash
# 1. Clone the repo
git clone https://github.com/your-org/carbon-platform.git
cd carbon-platform

# 2. Backend — with feature flags disabled (in-memory fallbacks used)
cd backend
python -m venv .venv && .venv\Scripts\activate    # Windows
# python -m venv .venv && source .venv/bin/activate  # macOS/Linux
pip install -r requirements-dev.txt

USE_OPENROUTER=false USE_SUPABASE=false USE_ANALYTICS=false USE_EVENT_QUEUE=false \
  uvicorn app.main:app --reload --port 8000

# 3. Frontend — in a separate terminal
cd frontend
npm install
npm run dev   # → http://localhost:5173 (proxies /api to :8000)
```

---

## Running Tests

```bash
# Backend tests with coverage
cd backend
pytest --cov=app --cov-report=term -v

# Frontend tests with coverage
cd frontend
npm test
```

---

## Deployment — Vercel + Container

### Frontend → Vercel

1. Import the repo into [vercel.com](https://vercel.com)
2. Set build command: `cd frontend && npm ci && npm run build`
3. Set output directory: `frontend/dist`
4. Add environment secrets (see `.env.example`)
5. Update the `/api/*` rewrite in `vercel.json` to point to your backend URL

### Backend → Docker / Any Container Host

```bash
# Build the image
docker build -t carbon-platform .

# Run locally
docker run -p 8080:8080 \
  -e OPENROUTER_API_KEY=your-key \
  -e SUPABASE_DB_URL=your-db-url \
  carbon-platform

# Or push to GHCR and deploy to Railway / Render / Fly.io
docker tag carbon-platform ghcr.io/your-org/carbon-platform:latest
docker push ghcr.io/your-org/carbon-platform:latest
```

### GitHub Actions (CI + Deploy)

The `.github/workflows/` directory contains:
- `ci.yml` — lint, typecheck, test, coverage, Docker build + health check
- `deploy.yml` — frontend to Vercel, backend image to GHCR

Required GitHub secrets:
| Secret | Purpose |
|---|---|
| `VERCEL_TOKEN` | Vercel deploy token |
| `VERCEL_ORG_ID` | Vercel organisation ID |
| `VERCEL_PROJECT_ID` | Vercel project ID |
| `VITE_API_BASE_URL` | Backend API URL for frontend build |

---

## Database Setup (Supabase / PostgreSQL)

Run the SQL migrations in order in your Supabase SQL Editor:

```
migrations/001_initial_schema.sql   — carbon_entries table
migrations/002_analytics_schema.sql — analytics_events, user_metrics, recommendation_logs
migrations/003_event_queue_schema.sql — event_queue table
```

Then set `SUPABASE_DB_URL` to your PostgreSQL connection string.

---

## Privacy & Security

- **No PII stored**: The `device_id` is a random session-scoped token — never a name, email, or real identifier.
- **Analytics never contain `device_id`**: Only aggregate stats (total_kg, diet_type, top_category).
- **Credentials via environment variables only**: No secrets in code. See `.env.example`.
- **Security checkpoint**: PII (SSNs, credit-card numbers) is scrubbed from AI prompts; prompt-injection attempts are blocked before reaching the LLM.
- **Security headers**: CSP, HSTS, X-Frame-Options, Permissions-Policy applied to every response.
- **Rate limiting**: 30/min calculate, 10/min insights, 20/min entries.

---

## Emission Factor Sources

| Factor | Source |
|--------|--------|
| Transport (car, bus, train) | UK DEFRA 2023 |
| Aviation (flights) | ICAO Carbon Calculator 2023 |
| Electricity | US EPA eGRID 2023 |
| Natural gas | UK DEFRA 2023 |
| Diet | Our World in Data 2023 (Poore & Nemecek 2018) |
| Consumption | IPCC AR6 WG3 Ch.5 |
| Global average (4,000 kg) | Our World in Data 2023 |
| Paris target (2,000 kg) | IPCC SR1.5 2018 |

---

## Accessibility

WCAG 2.1 AA compliant. All components tested with `jest-axe` (axe-core). See [ACCESSIBILITY_COMPLIANCE_REPORT.md](./ACCESSIBILITY_COMPLIANCE_REPORT.md).

Key features:
- Skip-to-main-content link
- All form inputs: `label` + `htmlFor` + `aria-describedby`
- Radio groups: `fieldset` + `legend`
- Charts: `role="img"` + screen-reader data table fallback
- Live regions: `aria-live="polite"` on results/insights
- Error alerts: `role="alert"` + `aria-live="assertive"`
- Keyboard navigation: all interactive elements focusable
- Reduced motion: `prefers-reduced-motion` respected

---

## Project Structure

```
carbon-platform/
├── backend/           FastAPI application
│   ├── app/
│   │   ├── carbon/    Pure emission calculation engine
│   │   ├── core/      Config, security, rate limiting
│   │   ├── models/    Pydantic v2 data models
│   │   ├── routes/    API endpoint handlers
│   │   └── services/  OpenRouter, Supabase, Analytics, EventQueue
│   └── tests/         pytest test suite
├── frontend/          React 18 + TypeScript SPA
│   ├── src/
│   │   ├── components/ Calculator, Insights, History, Shared
│   │   ├── store/      Zustand state management
│   │   ├── api/        Typed fetch client
│   │   └── utils/      Formatters and validators
│   └── tests/         Vitest + jest-axe test suite
├── migrations/        SQL migration files for Supabase/PostgreSQL
├── docs/              PRD, Architecture, Judge Evidence
├── Dockerfile         Multi-stage build
└── .github/           GitHub Actions CI + Deploy pipelines
```
