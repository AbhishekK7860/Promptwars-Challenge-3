# System Architecture Document
## ClimateIQ

---

## 1. High-Level Architecture

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                    Deployment Stack                     â”‚
â”‚                                                         â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”     â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”‚
â”‚  â”‚  Docker      â”‚â”€â”€â”€â”€â–ºâ”‚  OpenRouter (Gemini Flash)   â”‚  â”‚
â”‚  â”‚  Container   â”‚     â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜  â”‚
â”‚  â”‚              â”‚     â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”‚
â”‚  â”‚  FastAPI     â”‚â”€â”€â”€â”€â–ºâ”‚  Supabase PostgreSQL         â”‚  â”‚
â”‚  â”‚  Backend     â”‚     â”‚  (carbon_entries)            â”‚  â”‚
â”‚  â”‚              â”‚     â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜  â”‚
â”‚  â”‚              â”‚     â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”‚
â”‚  â”‚              â”‚â”€â”€â”€â”€â–ºâ”‚  analytics_events (Postgres) â”‚  â”‚
â”‚  â”‚              â”‚     â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜  â”‚
â”‚  â”‚              â”‚     â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”‚
â”‚  â”‚              â”‚â”€â”€â”€â”€â–ºâ”‚  event_queue (Postgres)      â”‚  â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜     â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜  â”‚
â”‚                                                         â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”   â”‚
â”‚  â”‚  GitHub Actions â”€â”€â–º GHCR â”€â”€â–º Container Host      â”‚   â”‚
â”‚  â”‚  GitHub Actions â”€â”€â–º Vercel (frontend SPA)        â”‚   â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜   â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
           â–²
           â”‚ HTTPS
           â”‚
    â”Œâ”€â”€â”€â”€â”€â”€â”´â”€â”€â”€â”€â”€â”€â”
    â”‚  Browser    â”‚
    â”‚  React SPA  â”‚
    â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

---

## 2. Container Architecture

**Multi-stage Dockerfile:**

```
Stage 1 (node:20-alpine)
  â””â”€â”€ npm ci â†’ npm run build â†’ /app/frontend/dist/

Stage 2 (python:3.11-slim)
  â”œâ”€â”€ pip install requirements.txt
  â”œâ”€â”€ COPY app/ â†’ /app/app/
  â”œâ”€â”€ COPY dist/ â†’ /app/static/
  â”œâ”€â”€ USER appuser (non-root)
  â””â”€â”€ CMD uvicorn app.main:app --workers 2 --port 8080
```

The single container serves:
- `GET /api/*` â†’ FastAPI routes
- `GET /assets/*` â†’ StaticFiles (Vite build)
- `GET /*` â†’ index.html (SPA fallback)

---

## 3. Request Flow: Carbon Calculation

```
Browser POST /api/calculate
    â”‚
    â–¼
FastAPI: SecurityHeadersMiddleware
    â”‚
    â–¼
FastAPI: CORSMiddleware
    â”‚
    â–¼
slowapi: Rate limit check (30/min/IP)
    â”‚
    â–¼
Pydantic: CarbonInput validation
    â”‚
    â–¼
calculator.calculate_footprint() â€” pure function, no I/O
    â”‚
    â–¼
Return CarbonResult (JSON)
```

---

## 4. Request Flow: Insights Generation

```
Browser POST /api/insights
    â”‚
    â–¼
FastAPI + slowapi (10/min/IP)
    â”‚
    â–¼
get_settings(): USE_GEMINI?
    â”‚
    â”œâ”€ YES â”€â”€â–º vertexai.GenerativeModel.generate_content()
    â”‚              â”œâ”€ SUCCESS â†’ parse JSON â†’ InsightItem[]
    â”‚              â””â”€ FAIL â†’ GeminiUnavailableError
    â”‚
    â””â”€ NO (or FAIL) â”€â”€â–º get_rule_based_insights()
                              â””â”€ Deterministic rules â†’ InsightItem[]
    â”‚
    â–¼
asyncio.create_task():
    â”œâ”€â”€ bigquery_service.log_event_async()  â† fire-and-forget
    â””â”€â”€ pubsub_service.publish_insight_request()  â† fire-and-forget
    â”‚
    â–¼
Return InsightsResponse { insights, source, total_potential_saving_kg }
```

---

## 5. Data Model

### Firestore: `carbon_entries/{docId}`
```json
{
  "device_id": "dev-lk3j2-abc123",
  "timestamp": "2024-01-15T12:00:00Z",
  "total_kg": 6800.0,
  "breakdown": {
    "transport": 3000.0,
    "home": 1300.0,
    "diet": 2500.0,
    "consumption": 1000.0
  },
  "ranked_categories": [...],
  "vs_global_average_pct": 170.0,
  "vs_paris_target_pct": 340.0,
  "insights": [...]
}
```

### BigQuery: `carbon_analytics.carbon_events`
```
timestamp       TIMESTAMP  â€” UTC event time
total_kg        FLOAT64    â€” total annual footprint
diet_type       STRING     â€” dietary pattern
insight_source  STRING     â€” "gemini" or "rules"
top_category    STRING     â€” highest-emission category
```
_Note: No `device_id` â€” privacy by design._

### Pub/Sub: `carbon-insights` topic
```json
{
  "footprint_total": 6800.0,
  "top_category": "transport",
  "timestamp": "2024-01-15T12:00:00Z"
}
```

---

## 6. Frontend State Management

```
Zustand Store
â”œâ”€â”€ inputs: Partial<CarbonInput>      â€” form values
â”œâ”€â”€ result: CarbonResult | null       â€” latest calculation
â”œâ”€â”€ insights: InsightsResponse | null â€” latest insights
â”œâ”€â”€ history: HistoryEntry[]           â€” all saved entries
â”œâ”€â”€ step: 'form' | 'results' | 'history'
â”œâ”€â”€ isCalculating / isLoadingInsights / isLoadingHistory
â””â”€â”€ error: string | null

Actions:
  calculate(inputs) â”€â”€â–º POST /api/calculate
  fetchInsights()   â”€â”€â–º POST /api/insights
  saveEntry()       â”€â”€â–º POST /api/entries
  fetchHistory()    â”€â”€â–º GET  /api/entries/{device_id}
```

---

## 7. Security Architecture

See [SECURITY_ARCHITECTURE.md](../SECURITY_ARCHITECTURE.md) for full details.

Key controls:
- **Authentication**: Application Default Credentials (ADC) â€” no API keys in code
- **Transport**: HTTPS-only via Cloud Run (TLS 1.2+)
- **Headers**: CSP, HSTS, X-Frame-Options, Permissions-Policy
- **Input validation**: Pydantic v2 (backend) + Zod (frontend)
- **Rate limiting**: slowapi per-IP
- **Firestore rules**: Create-only, field-validated
- **No PII**: device_id is cryptographically random, session-scoped
