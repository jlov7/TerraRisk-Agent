# TerraRisk Agent Quickstart: Get Started in Minutes

Welcome to TerraRisk Agent! This guide will help you get up and running quickly, whether you're a business analyst exploring AI-powered geospatial intelligence, a developer integrating the API, or a security professional evaluating governance frameworks.

**Note:** This is a personal R&D project—a passion-driven exploration of responsible AI agent development. It serves as a research platform and reference implementation, not a commercial product or business venture.

## What You'll Experience

When you run TerraRisk Agent, you'll get:
- **A live geospatial intelligence copilot** that answers complex questions using AI reasoning
- **Beautiful visualizations** of risk data on interactive maps
- **Auditable reports** with complete provenance tracking
- **Real-world examples** of responsible AI agent orchestration

**Time to first result:** About 5 minutes.

---

## For Non-Technical Users: The Easiest Path

### Step 1: Prerequisites
You need **Docker Desktop** installed and running. That's it!

- [Download Docker Desktop](https://www.docker.com/products/docker-desktop/) if you don't have it
- Make sure it's running (you'll see the Docker icon in your menu bar)

### Step 2: Launch the Demo
Open your terminal (or command prompt) and run:

```bash
cd ai-governance-suite
make demo-terra
```

**What this does:** Downloads and starts all necessary services (database, policy server, backend, frontend) in containers. No configuration needed!

### Step 3: Explore the Dashboard
Once you see "Ready!" messages, open your browser:

- **Dashboard**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs

**Try this:** Type a question like *"Which Gulf Coast counties have the highest hurricane risk?"* and watch the AI agent orchestrate multiple data sources to produce a comprehensive report.

### Step 4: View Results
- **Interactive Map**: See risk visualizations overlaid on geographic regions
- **Download Reports**: Get PDF summaries, GeoJSON layers, and CSV data
- **Provenance**: See exactly what data sources were used and how decisions were made

**That's it!** You're now exploring AI-powered geospatial intelligence.

---

## For Developers: Full Development Setup

### Option A: Use the Devcontainer (Recommended)

**Why this is easiest:** Everything is pre-configured—Python, Node.js, all tools, dependencies. Zero setup friction.

1. **Open in VS Code**:
   ```bash
   code ai-governance-suite
   ```

2. **Reopen in Container**:
   - VS Code will prompt: "Reopen in Container"
   - Or: Command Palette → "Dev Containers: Reopen in Container"
   - Wait for container to build (first time: ~5 minutes)

3. **You're ready!** All tools are installed:
   - Python 3.11+ with `uv`
   - Node.js 20+ with `pnpm`
   - `ruff`, `mypy`, `cosign`, `opa` (development tools)
   - Everything configured and working

### Option B: Local Setup

**Prerequisites:**
- Python 3.11+ (we recommend using `pyenv` or `asdf`)
- Node.js 20+ (we recommend using `nvm`)
- `uv` (Python package manager): `pip install uv` or `brew install uv`
- `pnpm`: `npm install -g pnpm`
- Docker Desktop (for running supporting services)

**Step 1: Clone and Navigate**
```bash
cd ai-governance-suite
```

**Step 2: Configure Environment**
```bash
cd apps/terrarisk-agent/backend
cp .env.example .env
# Edit .env if you want to customize settings
```

**Step 3: Start Supporting Services**
```bash
# From repository root
docker-compose up -d postgres redis opa otel-collector
```

**Step 4: Start Backend**
```bash
cd apps/terrarisk-agent/backend
uv sync  # Install dependencies
uv run uvicorn terrarisk.main:app --reload
```

Backend will be available at: http://localhost:8000

**Step 5: Start Frontend**
```bash
# In a new terminal
cd apps/terrarisk-agent/frontend
pnpm install
pnpm dev
```

Frontend will be available at: http://localhost:3000

---

## Understanding the Three Modes

TerraRisk Agent operates in three modes, each suited for different scenarios:

### 1. Offline Mode (Default)
**Best for:** Demos, development, testing

- **No cloud credentials needed**
- Uses synthetic data fixtures
- Fully reproducible results
- Perfect for exploring the system

**How to use:** Just run `make demo-terra`—it defaults to offline mode.

### 2. BYO BigQuery Mode
**Best for:** Organizations with existing Google Cloud BigQuery access

- **Bring your own GCP credentials**
- Real BigQuery Earth Engine queries
- Analyze your own portfolio data
- Earth AI remains stubbed (until API access is available)

**How to enable:**
```bash
# In apps/terrarisk-agent/backend/.env
GCP_PROJECT=your-project-id
BQ_DATASET=your-dataset
EARTHENGINE_PROJECT=your-project-id
```

**Authentication:** Use Application Default Credentials (`gcloud auth application-default login`) or a service account JSON file.

### 3. Cloud Mode (Full Integration)
**Best for:** Production deployments with full API access

- **Real Google Earth AI reasoning**
- Real BigQuery Earth Engine analytics
- Real FEMA NRI data queries
- Complete provenance tracking

**How to enable:**
```bash
# In apps/terrarisk-agent/backend/.env
EARTH_AI_ENABLED=1
GCP_PROJECT=your-project-id
BQ_DATASET=your-dataset
EARTHENGINE_PROJECT=your-project-id
# Add Earth AI API credentials when available
```

**Note:** Earth AI API access is currently limited—this mode is ready for when access expands.

---

## Your First Analysis

### Via the Web Interface

1. Open http://localhost:3000
2. Enter a query like: *"Which Gulf Coast counties have the highest hurricane risk this quarter?"*
3. Click "Analyze"
4. Watch the AI agent:
   - Decompose your question
   - Fetch data from multiple sources
   - Generate visualizations
   - Produce a signed report

### Via the API

**Using curl:**
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Which Gulf Coast counties show elevated hurricane risk?",
    "mode": "offline",
    "hazards": ["hurricane", "flood"],
    "geography_filter": ["22071", "12086"]
  }'
```

**Using Python:**
```python
import requests

response = requests.post(
    "http://localhost:8000/analyze",
    json={
        "query": "Which Gulf Coast counties show elevated hurricane risk?",
        "mode": "offline",
        "hazards": ["hurricane", "flood"]
    }
)

result = response.json()
print(f"Run ID: {result['run_id']}")
print(f"Artifacts: {[a['uri'] for a in result['artifacts']]}")
```

**Using the Interactive API Docs:**
1. Open http://localhost:8000/docs
2. Click "POST /analyze"
3. Click "Try it out"
4. Enter your query
5. Click "Execute"

---

## Exploring the API Endpoints

### Health Check
```bash
curl http://localhost:8000/healthz
```
Returns: `{"status": "ok", "mode": "offline"}`

### Analysis
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"query": "Your question here", "mode": "offline"}'
```

### Scenarios
Get quick scenario synopses for tabletop exercises:
```bash
# Hurricane scenario
curl http://localhost:8000/scenarios/hurricane

# Wildfire scenario
curl http://localhost:8000/scenarios/wildfire

# Flood scenario
curl http://localhost:8000/scenarios/flood
```

### Portfolio Stress Test
```bash
curl -X POST "http://localhost:8000/portfolio/stress?portfolio_id=demo-portfolio&mode=offline"
```

See [`docs/API_REFERENCE.md`](API_REFERENCE.md) for complete endpoint documentation.

---

## Viewing Generated Artifacts

When you run an analysis, TerraRisk Agent produces multiple artifacts:

### Location
**Default:** `apps/terrarisk-agent/backend/terrarisk/examples/artifacts/`

**Customize:** Set `ARTIFACT_DIR` environment variable:
```bash
export ARTIFACT_DIR=/tmp/terrarisk
uvicorn terrarisk.main:app --reload
```

### Artifact Types

1. **PDF Report** (`{run_id}_report.pdf`)
   - Human-readable analysis
   - Mitigation recommendations
   - Risk rankings
   - Action Credential metadata

2. **GeoJSON Layers** (`{run_id}_layers.geojson`)
   - Geographic visualizations
   - Risk overlays
   - Compatible with GIS tools and MapLibre

3. **CSV Portfolio Data** (`{run_id}_portfolio_diff.csv`)
   - Structured risk metrics
   - County-level rankings
   - Portfolio comparisons

### Viewing Artifacts

**GeoJSON:** Upload to [geojson.io](https://geojson.io) or use any GIS tool

**CSV:** Open in Excel, Google Sheets, or pandas

**PDF:** Open in any PDF viewer (includes provenance metadata)

---

## Running Quality Checks

### Backend Tests
```bash
cd apps/terrarisk-agent/backend
uv run pytest
```

### Linting & Type Checking
```bash
# Linting
uv run ruff check terrarisk

# Type checking
uv run mypy terrarisk
```

### Frontend Checks
```bash
cd apps/terrarisk-agent/frontend
pnpm lint
pnpm build
```

### Evaluation Harness
```bash
cd apps/terrarisk-agent/backend
uv run python ../evals/run_eval.py
```

**Target:** ROUGE-L F1 ≥ 0.75, 100% join integrity

### All Checks at Once
From repository root:
```bash
make qa
```

This runs:
- Backend tests
- Backend linting
- Backend type checking
- Frontend linting
- Frontend build
- Evaluation harness

---

## Troubleshooting

### "Docker not running"
**Solution:** Start Docker Desktop and wait for it to fully initialize.

### "Port already in use"
**Solution:** Change ports in `docker-compose.yml` or stop the conflicting service:
```bash
# Find what's using port 8000
lsof -i :8000
# Kill the process or change the port
```

### "Module not found" errors
**Solution:** Ensure dependencies are installed:
```bash
cd apps/terrarisk-agent/backend
uv sync
```

### "Frontend won't start"
**Solution:** Clear node_modules and reinstall:
```bash
cd apps/terrarisk-agent/frontend
rm -rf node_modules pnpm-lock.yaml
pnpm install
```

### "BigQuery authentication failed"
**Solution:** Ensure GCP credentials are configured:
```bash
gcloud auth application-default login
# Or set GOOGLE_APPLICATION_CREDENTIALS to service account JSON
```

---

## What's Next?

### For Business Users
- **[FAQ](FAQ.md)**: Common questions about governance, security, and use cases
- **[Architecture Overview](ARCHITECTURE.md)**: Understand how the system works
- **Explore the Dashboard**: Try different queries and scenarios

### For Developers
- **[Architecture Deep Dive](ARCHITECTURE.md)**: Understand the codebase structure
- **[API Reference](API_REFERENCE.md)**: Complete endpoint documentation
- **Read the Code**: Start with `backend/terrarisk/main.py` and `agents/planner.py`

### For Security Professionals
- **[Architecture](ARCHITECTURE.md)**: Review the governance and provenance sections
- **[FAQ](FAQ.md)**: Answers about policy enforcement and compliance
- **OPA Policies**: Explore `packages/policies/opa_bundle/policy.rego`

---

## Getting Help

- **Documentation**: All docs are in `docs/`
- **Code Issues**: Check the codebase—it's well-commented
- **Evaluation**: Run `make qa` to verify everything works

---

## Success Indicators

You know everything is working when:

✅ **Backend health check** returns `{"status": "ok", "mode": "offline"}`  
✅ **Frontend loads** at http://localhost:3000  
✅ **API docs** are interactive at http://localhost:8000/docs  
✅ **Analysis completes** and produces artifacts  
✅ **Evaluation harness** passes (ROUGE-L F1 ≥ 0.75)

**Congratulations!** You're now ready to explore AI-powered geospatial intelligence with full provenance tracking and governance.
