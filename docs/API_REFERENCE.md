# TerraRisk Agent API Reference

This reference explains the REST endpoints exposed by the FastAPI backend. Each section includes intent, payloads, sample responses, and notes for non-technical readers.

## Base URL
`http://localhost:8000` (when running locally via `make demo-terra` or `uvicorn`)

Swagger documentation: `http://localhost:8000/docs`

---

## Health Check
- **Endpoint**: `GET /healthz`
- **Purpose**: Verify the service is reachable and whether Earth AI mode is enabled.
- **Response**:
```json
{
  "status": "ok",
  "mode": "offline"
}
```
- **Who uses it**: Monitoring dashboards, analysts confirming the demo is online.

---

## Analyze
- **Endpoint**: `POST /analyze`
- **Purpose**: Run a full multi-step analysis and receive artifacts.
- **Request Body**:
```json
{
  "query": "Which Gulf Coast counties show elevated hurricane risk?",
  "mode": "offline",
  "hazards": ["hurricane", "flood"],
  "geography_filter": ["22071", "12086"],
  "portfolio_reference": "demo-portfolio"
}
```
- **Response (simplified)**:
```json
{
  "run_id": "abc123",
  "steps": [
    {"id": "earth-ai-1", "description": "Decompose query", "source": "earth_ai_stub", "inputs": ["Which Gulf Coast counties..."]},
    {"id": "...", "description": "Load FEMA NRI metrics", "source": "nri_loader", "inputs": []}
  ],
  "artifacts": [
    {"uri": ".../abc123_report.pdf", "type": "application/pdf"},
    {"uri": ".../abc123_layers.geojson", "type": "application/geo+json"},
    {"uri": ".../abc123_portfolio_diff.csv", "type": "text/csv"}
  ],
  "action_credentials": [
    {"id": "cred-1", "action": {"type": "planner.step.earth_ai_stub", "source": {"system": "earth_ai_stub"}}},
    {"id": "cred-2", "action": {"type": "report.compose", "source": {"system": "reports.compose"}}}
  ]
}
```
- **Notes for analysts**: The artifacts section lists where to find the generated report bundle. Action credentials provide provenance.

---

## Report (alias of Analyze)
- **Endpoint**: `POST /report`
- **Purpose**: Produce report artifacts; identical behavior to `/analyze`. Kept for semantic clarity when callers only want document generation.

---

## Scenarios
- **Endpoint**: `GET /scenarios/{hazard}`
- **Hazard Path Options**: `hurricane`, `flood`, `wildfire`
- **Purpose**: Request a quick scenario synopsis for tabletop exercises.
- **Response**:
```json
{
  "scenario": "hurricane",
  "summary": "Synthetic hurricane scenario for offline mode.",
  "metrics": {"risk_score": 0.7, "exposed_population": 125000},
  "recommended_actions": [
    "Pre-position mitigation assets",
    "Coordinate evacuation routes with local agencies",
    "Verify shelter capacity against population-at-risk"
  ],
  "artifacts": []
}
```
- **Who uses it**: Emergency managers rehearsing crises, or executives needing a concise briefing.

---

## Portfolio Stress
- **Endpoint**: `POST /portfolio/stress`
- **Query Parameters**:
  - `portfolio_id` (string): Identifier for the book of business.
  - `mode` (optional, defaults to `offline`): `cloud`, `byo_bigquery`, or `offline`.
- **Purpose**: Summarize stress metrics for a portfolio.
- **Response**:
```json
{
  "portfolio_id": "gulf-coast-portfolio",
  "summary": "Stress test for portfolio gulf-coast-portfolio in mode offline.",
  "metrics": {
    "pml": 0.82,
    "tail_value_at_risk": 0.21
  },
  "artifacts": []
}
```
- **Notes**: Metrics are synthetic today; replace with real computations once models integrate.

---

## Error Handling
- Standard FastAPI error envelopes are used (`{"detail": "error message"}`).
- When Earth AI is disabled by policy, expect HTTP 403 with explanatory detail once enforcement is wired in.

---

## Security & provenance reminders
- All artifact-generating endpoints produce action credentials ready for Sigstore/C2PA binding.
- OPA policies can be extended to gate endpoints depending on user role, budget, or geography precision.

Use this API reference to integrate the TerraRisk Agent with other systems, run scripted demos, or inform non-technical stakeholders about what the service offers and how outputs are authenticated.
