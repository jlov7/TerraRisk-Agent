# TerraRisk Agent (Personal R&D)

TerraRisk Agent is a personal passion R&D prototype that explores how an insurer/government copilot could orchestrate Google Earth AI's geospatial reasoning agent, BigQuery Earth Engine analytics, and FEMA National Risk Index data to produce bindable mitigation reports.

## Overview
- **API**: FastAPI service exposing `/analyze`, `/report`, `/scenarios/{hurricane|wildfire|flood}`, and `/portfolio/stress` endpoints.
- **Planner**: Multi-step decomposition merges Earth AI plans (stubbed today) with BigQuery Earth Engine templates and FEMA NRI joins.
- **Artifacts**: Bundles PDF placeholders, GeoJSON layers, CSV portfolio diffs, and mitigation highlights with Action Credentials (Sigstore-friendly schema).
- **Modes**:
  1. `cloud` – requires Earth AI access + BigQuery/Earth Engine roles.
  2. `byo_bigquery` – runs with customer-managed BigQuery only.
  3. `offline` – ships synthetic data and fixtures for demo parity.

### Documentation
- Quickstart guide: `docs/QUICKSTART.md`
- Architecture overview: `docs/ARCHITECTURE.md`
- API reference: `docs/API_REFERENCE.md`
- Frequently asked questions: `docs/FAQ.md`

## Getting Started
```bash
make demo-terra
```
This boots Postgres, Redis, OPA, the OTEL collector, and both backend/frontend containers. The frontend defaults to offline data until environment access is granted.

Copy `.env.example` to `.env` inside `apps/terrarisk-agent/backend/` if you want to tweak feature flags or configure real GCP resources.

### Local development
- Backend: `cd apps/terrarisk-agent/backend && uv run uvicorn terrarisk.main:app --reload`
- Frontend: `cd apps/terrarisk-agent/frontend && pnpm install && pnpm dev`

### Required credentials (cloud modes)
- `EARTH_AI_ENABLED=1` once Google Earth AI access is approved.
- `GCP_PROJECT`, `BQ_DATASET`, `EARTHENGINE_PROJECT` for BigQuery Earth Engine.
- Service account must hold `roles/bigquery.jobUser`, `roles/earthengine.resourceAdmin`, and read access to FEMA NRI tables.

### Example BigQuery Earth Engine SQL
```sql
SELECT
  county_fips,
  stats.mean_wind_speed
FROM ST_REGIONSTATS(
  (
    SELECT geom, county_fips FROM `project.dataset.county_boundaries`
  ),
  (
    SELECT * FROM `project.dataset.noaa_hurricane_wind`
  ),
  STRUCT(
    sample_size => 500,
    reducer => 'MEAN'
  )
);
```

### Provenance + Security
- Every planner/report step issues an Action Credential following `packages/schemas/action_credential_v0.json`.
- Artifacts are ready for Sigstore keyless signing and C2PA 2.2 manifests (soft-bound today).
- OPA bundle (`packages/policies/opa_bundle/policy.rego`) enforces deny-by-default, budget gates, and PII safeguards.
- OpenTelemetry traces ship to the local collector (`packages/otel/collector-config.yml`).
- Override report staging location with `ARTIFACT_DIR` if you need an alternate storage path during testing.

### Evaluations
- Golden Q&A, crisis scenarios, and joins integrity housed in `apps/terrarisk-agent/evals`.
- Offline fixtures (FEMA NRI slices, artifact staging) live under `apps/terrarisk-agent/backend/terrarisk/examples`.
- Target demo gate: ROUGE-L F1 ≥ 0.75 on offline Q&A, 100% join integrity on fixtures, reproducible report bundle checksums.
- Run the harness locally:
  ```bash
  cd apps/terrarisk-agent/backend
  uv run python ../evals/run_eval.py
  ```
- GitHub Actions CI runs the same evaluation gate after backend unit tests.
- Quick local sweep: `make qa` (backend tests, lint, type-checks, frontend lint, evaluation gate).

## References
- Google AI Blog — [Gemini powers Google Earth’s new AI tools (Oct 2023)](https://blog.google/technology/ai/google-earth-ai-oct-2023/)
- FEMA — [National Risk Index](https://hazards.fema.gov/nri/learn-more)
- Sigstore — [Keyless signing docs](https://docs.sigstore.dev/)
- C2PA — [Content Credentials 2.2 specification](https://c2pa.org/specifications/specifications)

## Roadmap
- Replace stubs with real Earth AI client once API access opens.
- Integrate BigQuery DataFrames for analytics and micro-batching.
- Expand mitigation playbooks with OPA policy insights and adjudication trails.
