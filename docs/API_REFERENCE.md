# TerraRisk Agent API Reference

Complete reference for the TerraRisk Agent REST API. This document explains every endpoint, request/response formats, error handling, and provides examples for both technical and non-technical users.

**Note:** This is a personal R&D project—a passion-driven exploration of responsible AI agent development. It serves as a research platform and reference implementation, not a commercial product or business venture.

## Base Information

**Base URL:** `http://localhost:8000` (when running locally)

**Interactive Documentation:** `http://localhost:8000/docs` (Swagger UI)

**API Version:** v1 (implicit)

**Content Type:** `application/json`

---

## Authentication

**Current Status:** No authentication required for demo/development mode.

**Future:** OAuth2/JWT tokens will be supported for production deployments. OPA policies will enforce authorization.

---

## Endpoints Overview

| Endpoint | Method | Purpose | Use Case |
|----------|--------|---------|----------|
| `/healthz` | GET | Health check | Monitoring, status verification |
| `/analyze` | POST | Full analysis workflow | Main entry point for geospatial queries |
| `/report` | POST | Generate report artifacts | Alias for `/analyze` (semantic clarity) |
| `/scenarios/{hazard}` | GET | Quick scenario summaries | Tabletop exercises, briefings |
| `/portfolio/stress` | POST | Portfolio stress testing | Risk assessment for insurance portfolios |

---

## Health Check

### `GET /healthz`

Verifies the service is running and reports operational mode.

**Use Cases:**
- Monitoring dashboards checking service availability
- Developers confirming the demo is online
- CI/CD pipelines verifying deployment success

**Request:**
```bash
curl http://localhost:8000/healthz
```

**Response:**
```json
{
  "status": "ok",
  "mode": "offline"
}
```

**Response Fields:**
- `status` (string): Always `"ok"` when service is healthy
- `mode` (string): Current operational mode (`"offline"`, `"byo_bigquery"`, or `"cloud"`)

**Error Responses:**
- `503 Service Unavailable`: Service is down or starting up

---

## Analysis (Main Endpoint)

### `POST /analyze`

Runs a complete multi-step geospatial analysis and produces signed artifacts with full provenance tracking.

**What It Does:**
1. Accepts a natural language query about geospatial risk
2. Decomposes the query into executable steps using AI reasoning
3. Orchestrates data fetching from multiple sources (FEMA NRI, BigQuery Earth Engine, etc.)
4. Generates reports, visualizations, and data exports
5. Produces Action Credentials for complete auditability

**Use Cases:**
- **Insurance Underwriters**: "Which counties have the highest hurricane risk?"
- **Emergency Planners**: "What's the wildfire risk scenario for California this quarter?"
- **Climate Analysts**: "Compare flood risk across three regions"

**Request:**

```json
{
  "query": "Which Gulf Coast counties show elevated hurricane risk?",
  "mode": "offline",
  "hazards": ["hurricane", "flood"],
  "geography_filter": ["22071", "12086"],
  "portfolio_reference": "demo-portfolio"
}
```

**Request Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `query` | string | ✅ Yes | Natural language question about geospatial risk |
| `mode` | enum | ❌ No | `"offline"` (default), `"byo_bigquery"`, or `"cloud"` |
| `hazards` | string[] | ❌ No | Hazard types: `["hurricane"]`, `["flood"]`, `["wildfire"]`, or combinations |
| `geography_filter` | string[] | ❌ No | County FIPS codes to filter analysis (e.g., `["22071"]` for Orleans Parish, LA) |
| `portfolio_reference` | string | ❌ No | Portfolio identifier for portfolio-level analysis |

**Example with curl:**
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Which Gulf Coast counties show elevated hurricane risk?",
    "mode": "offline",
    "hazards": ["hurricane", "flood"]
  }'
```

**Example with Python:**
```python
import requests

response = requests.post(
    "http://localhost:8000/analyze",
    json={
        "query": "Which Gulf Coast counties show elevated hurricane risk?",
        "mode": "offline",
        "hazards": ["hurricane", "flood"],
        "geography_filter": ["22071", "12086"]
    }
)

result = response.json()
print(f"Run ID: {result['run_id']}")
for artifact in result['artifacts']:
    print(f"  - {artifact['type']}: {artifact['uri']}")
```

**Response:**

```json
{
  "run_id": "550e8400-e29b-41d4-a716-446655440000",
  "steps": [
    {
      "id": "step-1",
      "description": "Decompose query into geospatial steps",
      "source": "earth_ai_stub",
      "inputs": ["Which Gulf Coast counties show elevated hurricane risk?"],
      "parameters": {}
    },
    {
      "id": "step-2",
      "description": "Load FEMA NRI metrics for requested geographies",
      "source": "nri_loader",
      "inputs": ["22071", "12086"],
      "parameters": {"hazards": ["hurricane", "flood"]}
    },
    {
      "id": "step-3",
      "description": "Join hazard metrics with BigQuery Earth Engine aggregations",
      "source": "bigquery_ee",
      "inputs": ["step-1", "step-2"],
      "parameters": {"mode": "offline"}
    },
    {
      "id": "step-4",
      "description": "Compose mitigation narrative and ranking",
      "source": "report_compose",
      "inputs": [],
      "parameters": {"portfolio_reference": "demo-portfolio"}
    }
  ],
  "artifacts": [
    {
      "uri": "file:///path/to/550e8400_report.pdf",
      "type": "application/pdf",
      "hash": "sha256:abc123..."
    },
    {
      "uri": "file:///path/to/550e8400_layers.geojson",
      "type": "application/geo+json",
      "hash": "sha256:def456..."
    },
    {
      "uri": "file:///path/to/550e8400_portfolio_diff.csv",
      "type": "text/csv",
      "hash": "sha256:789ghi..."
    }
  ],
  "action_credentials": [
    {
      "id": "cred-1",
      "action": {
        "type": "planner.step.earth_ai_stub",
        "source": {"system": "earth_ai_stub", "version": "1.0.0"}
      },
      "inputs": ["Which Gulf Coast counties..."],
      "outputs": ["step-1"],
      "timestamp": "2024-01-15T10:30:00Z"
    }
    // ... more credentials for each step
  ],
  "highlights": [
    "Orleans Parish (22071): EAL 0.85 with resilience index 0.42",
    "Miami-Dade County (12086): EAL 0.78 with resilience index 0.51"
  ],
  "sources": [
    "Synthetic Earth AI reasoning trace",
    "FEMA National Risk Index (offline fixture)",
    "BigQuery Earth Engine (template placeholders)"
  ]
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `run_id` | string (UUID) | Unique identifier for this analysis run |
| `steps` | array | Execution plan steps with provenance |
| `artifacts` | array | Generated artifacts (PDF, GeoJSON, CSV) |
| `action_credentials` | array | Full provenance chain for auditability |
| `highlights` | string[] | Key mitigation recommendations |
| `sources` | string[] | Data sources used in analysis |

**Error Responses:**

- `400 Bad Request`: Invalid request format or missing required fields
- `403 Forbidden`: Policy violation (e.g., Earth AI disabled, budget exceeded)
- `500 Internal Server Error`: Server error during analysis

**Processing Time:**
- Offline mode: ~2-5 seconds
- BYO BigQuery: ~10-30 seconds (depends on query complexity)
- Cloud mode: ~30-60 seconds (with Earth AI)

---

## Report (Alias)

### `POST /report`

Identical to `/analyze` but semantically clearer when you only want report generation.

**Use Case:** When integrating with systems that explicitly request "report generation" rather than "analysis."

**Request/Response:** Same as `/analyze`

---

## Scenarios

### `GET /scenarios/{hazard}`

Returns a quick scenario synopsis for tabletop exercises or executive briefings.

**Use Cases:**
- Emergency managers running tabletop exercises
- Executives needing concise risk briefings
- Risk analysts exploring hazard scenarios

**Path Parameters:**

| Parameter | Type | Options | Description |
|-----------|------|---------|-------------|
| `hazard` | enum | `hurricane`, `wildfire`, `flood` | Hazard type for scenario |

**Request Examples:**

```bash
# Hurricane scenario
curl http://localhost:8000/scenarios/hurricane

# Wildfire scenario
curl http://localhost:8000/scenarios/wildfire

# Flood scenario
curl http://localhost:8000/scenarios/flood
```

**Response:**

```json
{
  "scenario": "hurricane",
  "summary": "Synthetic hurricane scenario for offline mode. Demonstrates risk assessment workflow for Gulf Coast counties with elevated hurricane exposure.",
  "metrics": {
    "risk_score": 0.7,
    "exposed_population": 125000
  },
  "recommended_actions": [
    "Pre-position mitigation assets in high-risk counties",
    "Coordinate evacuation routes with local agencies",
    "Verify shelter capacity against population-at-risk"
  ],
  "artifacts": []
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `scenario` | string | Hazard type (hurricane, wildfire, flood) |
| `summary` | string | Human-readable scenario description |
| `metrics` | object | Key risk metrics (risk_score, exposed_population) |
| `recommended_actions` | string[] | Prioritized mitigation actions |
| `artifacts` | array | Generated artifacts (empty for scenarios) |

**Error Responses:**

- `404 Not Found`: Invalid hazard type (must be `hurricane`, `wildfire`, or `flood`)

---

## Portfolio Stress Test

### `POST /portfolio/stress`

Performs a stress test analysis for an insurance portfolio, calculating risk metrics like PML (Probable Maximum Loss) and Tail VaR.

**Use Cases:**
- Insurance actuaries assessing portfolio risk
- Risk managers evaluating exposure concentrations
- Underwriters comparing portfolio alternatives

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `portfolio_id` | string | ✅ Yes | Portfolio identifier |
| `mode` | enum | ❌ No | `"offline"` (default), `"byo_bigquery"`, or `"cloud"` |

**Request:**

```bash
curl -X POST "http://localhost:8000/portfolio/stress?portfolio_id=gulf-coast-portfolio&mode=offline"
```

**Response:**

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

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `portfolio_id` | string | Portfolio identifier |
| `summary` | string | Human-readable summary |
| `metrics` | object | Risk metrics (PML, Tail VaR, etc.) |
| `artifacts` | array | Generated artifacts (future: portfolio reports) |

**Metrics Explanation:**

- **PML (Probable Maximum Loss)**: Maximum expected loss at a given confidence level (0-1 scale)
- **Tail VaR (Tail Value at Risk)**: Expected loss beyond a certain threshold

**Note:** Metrics are synthetic in offline mode. Real computations require portfolio data integration.

**Error Responses:**

- `400 Bad Request`: Missing `portfolio_id` parameter
- `404 Not Found`: Portfolio not found (in cloud mode)

---

## Error Handling

### Standard Error Format

All errors follow FastAPI's standard error envelope:

```json
{
  "detail": "Human-readable error message"
}
```

### Common Error Codes

| Status Code | Meaning | Example |
|-------------|---------|---------|
| `400 Bad Request` | Invalid request format | Missing required field `query` |
| `403 Forbidden` | Policy violation | Earth AI disabled by policy |
| `404 Not Found` | Resource not found | Invalid hazard type |
| `500 Internal Server Error` | Server error | Database connection failed |

### Error Examples

**Missing Required Field:**
```json
{
  "detail": "Field 'query' is required"
}
```

**Policy Violation:**
```json
{
  "detail": "Earth AI access denied: feature flag disabled"
}
```

**Invalid Hazard:**
```json
{
  "detail": "Invalid hazard type 'tornado'. Must be one of: hurricane, wildfire, flood"
}
```

---

## Security & Provenance

### Action Credentials

Every analysis produces **Action Credentials** tracking:
- **Who/What**: System identifier and version
- **When**: ISO 8601 timestamp
- **Inputs**: What data was used
- **Outputs**: What was produced
- **Artifacts**: References to generated files

**Use Case:** Audit trails, compliance, reproducibility

### Sigstore Integration

Artifacts are ready for **Sigstore keyless signing**:
- No keys to manage
- OIDC authentication
- Rekor transparency log

**Example:**
```bash
# Sign an artifact
cosign sign-blob --yes artifact.pdf

# Verify signature
cosign verify-blob artifact.pdf
```

### C2PA Manifests

PDFs and images are designed for **C2PA (Content Credentials)** manifests:
- Embedded provenance metadata
- Verifiable authenticity
- Tamper detection

**Future Enhancement:** Full C2PA 2.2 manifest embedding in production PDFs

---

## Rate Limiting

**Current Status:** No rate limiting in demo/development mode.

**Future:** Rate limits will be enforced via OPA policies based on:
- User role
- Budget limits
- Geographic scope

---

## Best Practices

### For API Consumers

1. **Always check `/healthz` first** before making requests
2. **Use appropriate mode**: Offline for demos, BYO BigQuery for real data
3. **Handle errors gracefully**: Check status codes and error details
4. **Store run_ids**: Use for tracking and reproducibility
5. **Download artifacts promptly**: Files may be cleaned up after a period

### For Integration Developers

1. **Use async HTTP clients** for better performance
2. **Implement retry logic** for transient failures
3. **Cache scenario responses** (they're deterministic)
4. **Validate response schemas** before processing
5. **Log action_credentials** for audit trails

---

## Interactive API Documentation

**Swagger UI:** http://localhost:8000/docs

**ReDoc:** http://localhost:8000/redoc

**OpenAPI Schema:** http://localhost:8000/openapi.json

---

## Examples by Use Case

### Insurance Underwriting

```python
import requests

# Query hurricane risk for a portfolio
response = requests.post(
    "http://localhost:8000/analyze",
    json={
        "query": "Which Gulf Coast counties have the highest hurricane risk?",
        "mode": "offline",
        "hazards": ["hurricane"],
        "portfolio_reference": "gulf-coast-portfolio"
    }
)

result = response.json()
print(f"Analysis complete: {result['run_id']}")
print("\nHighlights:")
for highlight in result['highlights']:
    print(f"  - {highlight}")
```

### Emergency Planning

```python
# Get hurricane scenario for tabletop exercise
response = requests.get("http://localhost:8000/scenarios/hurricane")
scenario = response.json()

print(f"Scenario: {scenario['scenario']}")
print(f"Risk Score: {scenario['metrics']['risk_score']}")
print("\nRecommended Actions:")
for action in scenario['recommended_actions']:
    print(f"  - {action}")
```

### Portfolio Risk Assessment

```python
# Stress test a portfolio
response = requests.post(
    "http://localhost:8000/portfolio/stress",
    params={
        "portfolio_id": "gulf-coast-portfolio",
        "mode": "offline"
    }
)

stress = response.json()
print(f"Portfolio: {stress['portfolio_id']}")
print(f"PML: {stress['metrics']['pml']}")
print(f"Tail VaR: {stress['metrics']['tail_value_at_risk']}")
```

---

This API reference provides everything you need to integrate TerraRisk Agent into your workflows. For architecture details, see [`ARCHITECTURE.md`](ARCHITECTURE.md). For common questions, see [`FAQ.md`](FAQ.md).
