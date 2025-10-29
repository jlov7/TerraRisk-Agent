# TerraRisk Agent: AI-Powered Geospatial Intelligence

TerraRisk Agent is a complete implementation demonstrating how to build **trustworthy AI agents** for geospatial intelligence. It combines Google Earth AI's reasoning capabilities, FEMA National Risk Index data, and BigQuery Earth Engine analytics to produce auditable, signed reports with complete provenance tracking.

## What Makes TerraRisk Agent Special

**For Business Users:**
- Ask complex geospatial questions in natural language
- Get comprehensive risk analyses in minutes instead of days
- Trust every output—complete audit trails and verifiable signatures

**For Technical Users:**
- Reference implementation for responsible AI agent orchestration
- Demonstrates provenance tracking, policy enforcement, and observability
- Modern stack ready for extension and production deployment

**For Security Professionals:**
- Policy-driven governance with OPA/Rego bundles
- Action Credentials for complete audit trails
- Sigstore and C2PA integration ready

## Quick Start

**Demo Mode (No Code Required):**
```bash
cd ai-governance-suite
make demo-terra
```

Opens dashboard at http://localhost:3000 and API at http://localhost:8000/docs

**Developer Mode:**
```bash
# Backend
cd apps/terrarisk-agent/backend
uv run uvicorn terrarisk.main:app --reload

# Frontend (new terminal)
cd apps/terrarisk-agent/frontend
pnpm install && pnpm dev
```

See [`docs/QUICKSTART.md`](../docs/QUICKSTART.md) for detailed setup instructions.

## Architecture Overview

```
User Query → Planner Agent → Connectors → Governance → Reports
                                    ↓
                          Action Credentials (Provenance)
```

**Key Components:**

- **API Layer**: FastAPI REST endpoints for analysis, scenarios, portfolio stress tests
- **Planner Agent**: Multi-step decomposition combining Earth AI reasoning with data joins
- **Connectors**: Modular clients for Earth AI, BigQuery, FEMA NRI, boundaries
- **Services**: Orchestrates execution, ranks hazards, generates deliverables
- **Reports**: PDF, GeoJSON, CSV generation with Action Credentials
- **Frontend**: Next.js dashboard with interactive map visualization
- **Governance**: OPA policies, Action Credentials, provenance tracking

See [`docs/ARCHITECTURE.md`](../docs/ARCHITECTURE.md) for complete system design.

## Features

### Three Operational Modes

1. **Offline Mode** (default): Synthetic fixtures—perfect for demos without cloud credentials
2. **BYO BigQuery**: Use your own BigQuery/Earth Engine—Earth AI remains stubbed until API access is available
3. **Cloud Mode**: Full integration with Earth AI + BigQuery—requires API access

### Built-in Governance

- **Policy Enforcement**: Deny-by-default with OPA/Rego bundles
- **Budget Controls**: Prevent runaway API costs
- **PII Safeguards**: County-level granularity by default
- **Feature Flags**: Control access to experimental capabilities

### Complete Observability

- OpenTelemetry traces for every analysis
- Action Credentials for every decision
- Reproducible artifact checksums
- Evaluation gates for quality assurance

## API Endpoints

- **`POST /analyze`**: Run full geospatial analysis
- **`POST /report`**: Generate report artifacts (alias for `/analyze`)
- **`GET /scenarios/{hazard}`**: Quick scenario summaries (hurricane, wildfire, flood)
- **`POST /portfolio/stress`**: Portfolio stress testing
- **`GET /healthz`**: Health check

See [`docs/API_REFERENCE.md`](../docs/API_REFERENCE.md) for complete endpoint documentation.

## Example Use Cases

### Insurance Underwriting
*"Which Gulf Coast counties have the highest hurricane risk?"*
→ Produces risk rankings, mitigation recommendations, portfolio stress metrics

### Emergency Planning
*"What's the wildfire risk scenario for California this quarter?"*
→ Generates scenario summary with recommended actions and visualizations

### Climate Risk Analysis
*"Compare flood risk across three different regions."*
→ Creates comparative analysis with signed, verifiable reports

## Generated Artifacts

Every analysis produces:

1. **PDF Report**: Human-readable analysis with mitigation recommendations
2. **GeoJSON Layers**: Visualizable geographic data for GIS tools
3. **CSV Portfolio Data**: Structured risk metrics for analysis
4. **Action Credentials**: Complete provenance chain for auditability

**Location**: `apps/terrarisk-agent/backend/terrarisk/examples/artifacts/`

**Customize**: Set `ARTIFACT_DIR` environment variable

## Quality Assurance

**Evaluation Harness:**
```bash
cd apps/terrarisk-agent/backend
uv run python ../evals/run_eval.py
```

**Target Metrics:**
- ROUGE-L F1 ≥ 0.75 (narrative quality)
- Join integrity: 100% (data correctness)
- Reproducible artifact checksums

**All Checks:**
```bash
make qa  # Runs tests, lint, type-check, eval harness
```

## Configuration

**Environment Variables:**
- `EARTH_AI_ENABLED`: Enable Earth AI integration (requires API access)
- `GCP_PROJECT`: Google Cloud project ID
- `BQ_DATASET`: BigQuery dataset name
- `EARTHENGINE_PROJECT`: Earth Engine project ID
- `ARTIFACT_DIR`: Custom artifact storage location

**See:** `apps/terrarisk-agent/backend/.env.example`

## Documentation

- **[Quickstart Guide](../docs/QUICKSTART.md)**: Get up and running in minutes
- **[Architecture Deep Dive](../docs/ARCHITECTURE.md)**: Complete system design
- **[API Reference](../docs/API_REFERENCE.md)**: Endpoint documentation
- **[FAQ](../docs/FAQ.md)**: Common questions answered
- **[Appendices](../docs/APPENDICES.md)**: Reference materials

## Project Structure

```
apps/terrarisk-agent/
├── backend/              # FastAPI service
│   ├── terrarisk/
│   │   ├── agents/       # Planner agent
│   │   ├── connectors/   # Data source clients
│   │   ├── services/     # Business logic
│   │   ├── reports/      # Report generation
│   │   └── models/       # Domain models
│   └── tests/            # Unit tests
├── frontend/             # Next.js dashboard
│   ├── app/              # Next.js app router
│   ├── components/       # React components
│   └── lib/              # API client, types
└── evals/                # Evaluation harness
    ├── golden_qa.jsonl   # Golden Q&A test cases
    └── run_eval.py       # Evaluation script
```

## Why This Matters

**In the Age of AI Agents:**
- AI agents are revolutionizing geospatial analysis
- But trust requires provenance, auditability, and governance
- TerraRisk Agent demonstrates how to build responsible AI systems

**For Regulated Industries:**
- Insurance, finance, government need auditable AI
- Action Credentials provide complete decision trails
- OPA policies enforce compliance at runtime

**For the AI Community:**
- Reference implementation for multi-agent orchestration
- Demonstrates provenance tracking patterns
- Shows how to integrate governance into AI workflows

## References

- [Google Earth AI](https://blog.google/technology/ai/google-earth-ai-oct-2023/) - Geospatial reasoning agents
- [FEMA National Risk Index](https://hazards.fema.gov/nri/learn-more) - Comprehensive hazard data
- [Sigstore](https://docs.sigstore.dev/) - Keyless signing for software supply chain
- [C2PA](https://c2pa.org/specifications/specifications) - Content Credentials for media provenance
- [Open Policy Agent](https://www.openpolicyagent.org/) - Policy-as-code enforcement

---

**Built as a research platform to explore responsible AI agent development. Use it as a reference, extend it responsibly, and contribute to the future of trustworthy AI.**
