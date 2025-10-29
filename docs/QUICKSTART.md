# TerraRisk Agent Quickstart

Welcome! This guide walks both technical and non-technical collaborators through standing up the TerraRisk Agent R&D environment in minutes.

## 1. What you get
- FastAPI backend that orchestrates synthetic Earth AI plans, FEMA NRI slices, and BigQuery Earth Engine templates.
- Next.js frontend for running analyses, viewing map overlays, and downloading report bundles.
- Reproducible offline fixtures so you can demo without Google Cloud credentials.

## 2. Prerequisites
| Role | Requirement | Notes |
| --- | --- | --- |
| Analyst / Non-technical | Docker Desktop OR ability to run `make demo-terra` | No coding required. |
| Engineer | Docker, Python 3.11+, Node 20, pnpm, Make | Use devcontainer for hands-free setup. |
| Security / Gov Analyst | Optional: cosign, opa CLIs | Already baked into devcontainer. |

Before running in developer mode, copy `apps/terrarisk-agent/backend/.env.example` to `.env` and adjust feature flags or GCP credentials as needed.

## 3. Launch the demo (no code)
```bash
cd ai-governance-suite
make demo-terra
```
- Backend: http://localhost:8000/docs (FastAPI Swagger UI).
- Frontend: http://localhost:3000 (TerraRisk dashboard).
- Login not required; fixtures are synthetic.

## 4. Run locally as a developer
```bash
# Backend (FastAPI with auto-reload)
cd apps/terrarisk-agent/backend
uv run uvicorn terrarisk.main:app --reload

# Frontend
cd ../frontend
pnpm install
pnpm dev
```

## 5. Toggle operational modes
- Offline (default): no Google Cloud access needed.
- BYO BigQuery: set `GCP_PROJECT`, `BQ_DATASET`, `EARTHENGINE_PROJECT`.
- Cloud (Earth AI + BigQuery): also set `EARTH_AI_ENABLED=1` and provide Earth AI credentials once available.

## 6. Run automated checks
```bash
cd apps/terrarisk-agent/backend
uv run pytest
uv run ruff check terrarisk
uv run mypy terrarisk

cd ../frontend
pnpm lint
pnpm build
```

From the repository root you can also run `make qa` to execute backend tests, lint, type checks, frontend lint, and the ROUGE-L evaluation gate in one command.

## 7. Generate a synthetic report
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"query": "Where is hurricane + flood risk highest this quarter?", "mode": "offline"}'
```
Artifacts (PDF/GeoJSON/CSV) are stored in `apps/terrarisk-agent/backend/terrarisk/examples/artifacts` by default. Override with `ARTIFACT_DIR=/tmp/terrarisk`.

## 8. What's next?
- Review the architecture overview (`docs/ARCHITECTURE.md`) to understand service boundaries.
- Dive into the API reference (`docs/API_REFERENCE.md`) when integrating other tools.
- Share the FAQ (`docs/FAQ.md`) with stakeholders to answer governance questions.
