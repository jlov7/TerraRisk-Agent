# TerraRisk Agent Architecture: Building Trustworthy Geospatial AI Agents

This document explains how TerraRisk Agent works—from a high-level story that anyone can understand, to technical deep-dives for developers. Whether you're an executive evaluating AI solutions, an analyst using the system, or an engineer extending it, this guide will help you understand the architecture.

**Note:** This is a personal R&D project—a passion-driven exploration of responsible AI agent development. It serves as a research platform and reference implementation, not a commercial product or business venture.

## The Big Picture: Why This Architecture Matters

Imagine you're an insurance underwriter assessing hurricane risk for properties along the Gulf Coast. You need to:
1. Understand the natural language question: *"Which counties have the highest hurricane risk this quarter?"*
2. Decompose it into actionable steps: query FEMA data, analyze satellite imagery, join with portfolio data
3. Produce a report that's **auditable**, **verifiable**, and **trustworthy**

Traditional geospatial analysis requires deep expertise and takes days. **AI agents can do this in minutes**—but only if we can trust their outputs. This architecture demonstrates how to build that trust through:

- **Provenance tracking**: Every decision is recorded with Action Credentials
- **Policy enforcement**: OPA policies ensure compliance and security
- **Audit trails**: Complete history of who did what, when, and why
- **Signed outputs**: Reports can be cryptographically verified

---

## The User Journey: From Question to Report

### Step 1: The User Asks a Question
```
User: "Which Gulf Coast counties show elevated hurricane risk?"
```

### Step 2: The Planner Decomposes the Problem
The planner agent (inspired by Google Earth AI's reasoning capabilities) breaks this down into:
- **Earth AI Step**: "Identify Gulf Coast counties with historical hurricane patterns"
- **FEMA NRI Step**: "Load risk metrics for identified counties"
- **BigQuery Step**: "Join with Earth Engine satellite data for current conditions"
- **Report Step**: "Generate mitigation recommendations and rankings"

### Step 3: Connectors Fetch Data
Each connector handles a specific data source:
- **Earth AI**: Geospatial reasoning (currently stubbed, ready for real API)
- **FEMA NRI**: National Risk Index data (offline fixtures available)
- **BigQuery Earth Engine**: Satellite imagery and analytics
- **Boundaries**: Geographic boundary data

### Step 4: Governance Layer Validates
Before any action executes:
- **OPA Policies** check: Is this user authorized? Is the budget sufficient? Is PII being accessed?
- **Action Credentials** are created: Tracking inputs, outputs, timestamps, and provenance

### Step 5: Report Generation
The system produces:
- **PDF Report**: Human-readable analysis with recommendations
- **GeoJSON Layers**: Visualizable geographic data
- **CSV Portfolio Data**: Structured risk metrics
- **Signed Artifacts**: Cryptographically verifiable outputs

**Every output is traceable back to the original query, data sources, and reasoning steps.**

---

## Core Components Explained

### For Non-Technical Readers

| Component | What It Does | Why It Matters |
|-----------|--------------|----------------|
| **API Layer** | The "front door" that receives your questions | Makes the system accessible via web interface or API calls |
| **Planner** | The "brain" that breaks down complex questions | Understands what you're asking and figures out how to answer it |
| **Connectors** | The "data gatherers" that fetch information | Pulls data from FEMA, Google Earth, satellite imagery, etc. |
| **Services** | The "orchestrator" that coordinates everything | Makes sure all the pieces work together smoothly |
| **Reports** | The "output generator" that creates your deliverables | Produces PDFs, maps, spreadsheets you can use |
| **Frontend** | The "dashboard" you interact with | Visual interface to ask questions and see results |
| **Governance** | The "safety layer" that ensures compliance | Makes sure everything is auditable and secure |

### For Technical Readers

| Layer | Purpose | Implementation | Key Files |
|-------|---------|----------------|-----------|
| **API** | RESTful endpoints for analysis, scenarios, portfolio stress tests | FastAPI with OpenAPI docs | `backend/terrarisk/main.py` |
| **Planner** | Multi-step decomposition combining Earth AI reasoning with data joins | Graph-based execution planning | `backend/terrarisk/agents/planner.py` |
| **Connectors** | Modular data clients for Earth AI, BigQuery, FEMA NRI, boundaries | Abstraction layer with offline/cloud modes | `backend/terrarisk/connectors/*.py` |
| **Services** | Orchestrates planner output, executes joins, ranks hazards | Business logic layer | `backend/terrarisk/services/analysis.py` |
| **Reports** | PDF, GeoJSON, CSV generation with provenance | Document generation with C2PA-ready manifests | `backend/terrarisk/reports/compose.py` |
| **Frontend** | Next.js dashboard with map visualization | React-based UI with MapLibre | `frontend/app/page.tsx`, `frontend/components/MapPreview.tsx` |
| **Governance** | OPA policies, Action Credentials, provenance tracking | Policy enforcement and audit logging | `packages/policies/`, `packages/schemas/` |
| **Eval Harness** | Quality assurance via golden Q&A and integrity checks | ROUGE-L F1 scoring, join validation | `evals/run_eval.py` |

---

## Data Flow: How Information Moves Through the System

```
┌─────────────────────────────────────────────────────────────┐
│                    User Query                               │
│          "Which Gulf Coast counties have highest             │
│           hurricane risk this quarter?"                      │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│              AnalysisRequest Model                            │
│  • query: natural language question                          │
│  • mode: offline | byo_bigquery | cloud                      │
│  • hazards: [hurricane, flood, wildfire]                    │
│  • geography_filter: [county_fips codes]                     │
│  • portfolio_reference: optional portfolio ID                │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                    Planner Agent                             │
│                                                               │
│  1. Earth AI Stub: "Decompose query into geospatial steps"  │
│  2. NRI Loader: "Load FEMA risk metrics"                    │
│  3. BigQuery EE: "Join with Earth Engine data"               │
│  4. Report Compose: "Generate mitigation narrative"          │
│                                                               │
│  Each step produces:                                         │
│  • PlannerStep with ID, description, source, inputs           │
│  • ActionCredential for provenance                          │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                    Connectors Execute                        │
│                                                               │
│  Earth AI Client:                                           │
│  • Stub mode: Returns synthetic plan steps                   │
│  • Cloud mode: Calls Google Earth AI API                     │
│                                                               │
│  NRI Loader:                                                 │
│  • Offline: Reads CSV fixtures                               │
│  • Cloud: Queries FEMA NRI tables                           │
│                                                               │
│  BigQuery EE:                                                │
│  • Template queries for satellite data                       │
│  • ST_REGIONSTATS for geospatial aggregations                │
│                                                               │
│  Boundary Provider:                                          │
│  • GeoJSON for county boundaries                             │
│  • MapLibre-compatible features                              │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                    Governance Layer                          │
│                                                               │
│  OPA Policy Check (for each step):                          │
│  • Is Earth AI enabled?                                      │
│  • Is budget sufficient?                                      │
│  • Is geography granularity acceptable?                      │
│  • Is PII access authorized?                                 │
│                                                               │
│  Action Credential Creation:                                 │
│  • action_type: "planner.step.{source}"                      │
│  • inputs: [step IDs, query, parameters]                    │
│  • outputs: [generated artifacts]                            │
│  • source: system identifier                                 │
│  • timestamp: ISO 8601                                       │
│  • artifacts: [PDF, GeoJSON, CSV URIs]                       │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                    Analysis Service                          │
│                                                               │
│  1. Execute planner steps in dependency order                │
│  2. Rank hazards by EAL (Expected Annual Loss)               │
│  3. Generate mitigation highlights                           │
│  4. Create portfolio diff CSV                                │
│  5. Produce GeoJSON layers                                   │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                    Report Composer                           │
│                                                               │
│  Artifacts Generated:                                        │
│  • {run_id}_report.pdf                                       │
│  • {run_id}_layers.geojson                                   │
│  • {run_id}_portfolio_diff.csv                              │
│                                                               │
│  Each artifact:                                              │
│  • Includes Action Credential metadata                       │
│  • Ready for Sigstore signing                                │
│  • C2PA manifest ready (when PDFs are enhanced)             │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                    AnalysisResponse                          │
│                                                               │
│  • run_id: unique identifier                                 │
│  • steps: [PlannerStep with credentials]                     │
│  • artifacts: [Artifact URIs]                                │
│  • action_credentials: [full provenance chain]               │
│  • highlights: [mitigation recommendations]                  │
│  • sources: [data source citations]                          │
└─────────────────────────────────────────────────────────────┘
```

---

## Modes of Operation: Flexibility for Different Needs

### Offline Mode (Default)
**Perfect for:** Demos, development, testing without cloud dependencies

- Synthetic Earth AI plans (stubbed responses)
- FEMA NRI fixtures (sample counties)
- No external API calls required
- Fully reproducible results

**Use case:** "I want to see how this works without setting up Google Cloud credentials."

### BYO BigQuery Mode
**Perfect for:** Organizations with existing BigQuery/Earth Engine access

- Bring your own GCP credentials
- Real BigQuery Earth Engine queries
- Earth AI remains stubbed (until API access is available)
- Portfolio data from your BigQuery tables

**Use case:** "I have BigQuery access and want to analyze my portfolio, but Earth AI isn't available yet."

### Cloud Mode
**Perfect for:** Production deployments with full API access

- Real Google Earth AI reasoning
- Real BigQuery Earth Engine analytics
- Real FEMA NRI data queries
- Full provenance tracking

**Use case:** "I have Earth AI access and want the complete, production-ready experience."

**Configuration:** Set `EARTH_AI_ENABLED=1` and provide appropriate credentials.

---

## Data Provenance: Building Trust Through Transparency

### What Is Provenance?
**Provenance** means "where did this come from?" For AI agents, it means:
- What data sources were used?
- What reasoning steps were taken?
- Who or what made each decision?
- When did it happen?
- Can we reproduce this result?

### Action Credentials: The Building Blocks

Every step in TerraRisk Agent produces an **Action Credential** following the A2PA (AI Agent Provenance Architecture) schema:

```json
{
  "id": "cred-abc123",
  "action": {
    "type": "planner.step.earth_ai_stub",
    "source": {"system": "earth_ai_stub", "version": "1.0.0"}
  },
  "inputs": ["query: Which Gulf Coast counties..."],
  "outputs": ["step-id-xyz789"],
  "artifacts": [
    {"uri": ".../report.pdf", "type": "application/pdf", "hash": "sha256:..."}
  ],
  "claims": [
    {"name": "description", "value": "Decompose query into geospatial steps"}
  ],
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Why This Matters

**For Business Users:**
- **Audit Compliance**: "Who approved this analysis? Show me the decision trail."
- **Reproducibility**: "Can we run this exact analysis again with the same results?"
- **Trust**: "I can verify this report hasn't been tampered with."

**For Technical Users:**
- **Debugging**: Trace execution through the entire workflow
- **Evaluation**: Measure quality and correctness
- **Integration**: Chain multiple analyses together

### Signing & Verification

Action Credentials are designed for **Sigstore keyless signing**:
- No keys to manage—uses OIDC authentication
- Rekor transparency log for public verification
- C2PA manifests for media artifacts (PDFs, images)

**Example workflow:**
```bash
# Generate credential
action_credential = create_action_credential(...)

# Sign with Sigstore (keyless)
cosign sign-blob --yes credential.json

# Verify signature
cosign verify-blob credential.json
```

---

## Security Posture: Policy-Driven Governance

### Deny-by-Default Philosophy
**Everything is blocked unless explicitly allowed.** This is enforced through OPA (Open Policy Agent) policies.

### Policy Enforcement Points

1. **Feature Flags**: Is Earth AI enabled for this user/role?
2. **Budget Limits**: Has this analysis exceeded the cost threshold?
3. **Geography Granularity**: County-level okay, but block street-level to prevent PII exposure
4. **Approval Workflows**: Certain actions require explicit approval

### OPA Policy Example

```rego
# Deny Earth AI if not enabled
default allow_earth_ai = false
allow_earth_ai {
    input.feature_flags.earth_ai_enabled == true
    input.user.role == "analyst"
}

# Enforce budget limits
deny {
    input.analysis.cost_estimate > input.user.budget_limit
}
```

### Extending Policies

You can extend policies for:
- **Per-tool approvals**: Require approval before calling specific connectors
- **Time-based restrictions**: Only allow analyses during business hours
- **Data residency**: Ensure data stays within certain geographic boundaries
- **Windows MCP mediation**: Integrate with Microsoft's Model Context Protocol

---

## Developer Experience: Making It Easy to Build

### Devcontainer Setup
Everything is pre-configured in the devcontainer:
- Python 3.11+ with `uv` package manager
- Node.js 20+ with `pnpm`
- Development tools: `ruff`, `mypy`, `cosign`, `opa`
- Go toolchain (for OPA policy development)

**Just open in VS Code or GitHub Codespaces**—everything works.

### Docker Compose Orchestration
One command starts everything:
```bash
make demo-terra
```

This launches:
- PostgreSQL (for future stateful scenarios)
- Redis (for caching)
- OPA (policy server)
- OpenTelemetry Collector (for observability)
- Backend (FastAPI service)
- Frontend (Next.js dashboard)

### Make Targets
- `make demo-terra`: Launch full stack
- `make qa`: Run all quality checks (tests, lint, type-check, eval)
- `make dev`: Development mode with hot reload

---

## Extension Points: How to Customize

### Adding New Connectors
1. Create a new connector in `backend/terrarisk/connectors/`
2. Implement the connector interface (load data, return structured results)
3. Add it to the planner steps
4. Create offline fixtures for demo mode

**Example:** Add a connector for NOAA weather data
```python
# backend/terrarisk/connectors/noaa.py
class NOAAClient:
    def load_weather_data(self, geography: str) -> WeatherData:
        # Implementation
        pass
```

### Adding New Hazards
1. Extend `HazardType` enum in `models/domain.py`
2. Add scenario logic in `main.py` scenarios endpoint
3. Update NRI loader to handle new hazard type
4. Add evaluation fixtures

### Integrating Other AI Frameworks
The architecture is designed to support:
- **Microsoft Agent Framework**: Via adapter pattern
- **OpenAI AgentKit**: Via connector interface
- **Mistral Agents**: Via planner abstraction

**Pattern:** Create an adapter that translates TerraRisk's `PlannerStep` format to the target framework's format.

---

## Observability: Understanding What's Happening

### OpenTelemetry Integration
Every analysis produces OpenTelemetry traces:
- **Trace ID**: Unique identifier for the entire analysis
- **Spans**: Individual steps (planner, connectors, reports)
- **Attributes**: Metadata (user, mode, query, geography)

**Future Enhancement:** Thread trace IDs into Action Credentials for complete correlation.

### Logging
Structured logging captures:
- Analysis requests and responses
- Policy decisions (allow/deny)
- Connector execution (success/failure)
- Report generation status

### Metrics (Future)
- Analysis latency
- Connector success rates
- Policy denials
- Artifact generation time

---

## Limitations & Future Work

### Current Limitations

1. **Earth AI is Stubbed**: Real Google Earth AI integration awaits API access
2. **PDFs are Placeholder**: Production should use WeasyPrint templates with C2PA manifests
3. **Deterministic Planner**: Will incorporate dynamic reasoning once Earth AI is available
4. **No Persistence**: Postgres is reserved for future stateful scenarios

### Roadmap

**Near-term:**
- Real Earth AI client integration
- Enhanced PDF generation with C2PA
- BigQuery DataFrames for analytics
- Expanded mitigation playbooks

**Long-term:**
- Windows MCP mediation support
- Multi-agent orchestration patterns
- Advanced evaluation metrics
- Production deployment guides

---

## Key Takeaways

### For Executives
- **Trust**: Every output is auditable and verifiable
- **Compliance**: Built-in governance and policy enforcement
- **Scalability**: Architecture supports multiple data sources and AI frameworks
- **Risk Management**: Deny-by-default security posture

### For Analysts
- **Natural Language Interface**: Ask questions in plain language
- **Fast Results**: Minutes instead of days
- **Reproducible**: Run the same analysis again with identical results
- **Transparent**: See exactly what data sources were used

### For Engineers
- **Modular Design**: Easy to extend with new connectors
- **Modern Stack**: FastAPI, Next.js, OpenTelemetry, containerized
- **Proven Patterns**: Action Credentials, OPA policies, Sigstore signing
- **Production-Ready**: All the infrastructure for regulated industries

---

This architecture demonstrates how to build **AI agents that are powerful, responsible, and trustworthy**. It's a blueprint for the future of geospatial intelligence—where AI accelerates decision-making while maintaining complete transparency and accountability.
