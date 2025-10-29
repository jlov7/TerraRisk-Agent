# TerraRisk Agent FAQ: Common Questions Answered

Frequently asked questions about TerraRisk Agent, covering everything from basic concepts to governance, security, and deployment. Organized for both technical and non-technical audiences.

---

## General Questions

### What is TerraRisk Agent?

**Simple Answer:** TerraRisk Agent is an AI-powered geospatial intelligence copilot that helps answer complex questions about climate risk, natural hazards, and geographic analysis. Think of it as a smart assistant that combines AI reasoning with real-world data sources to produce trustworthy, auditable reports.

**Technical Answer:** TerraRisk Agent is a research platform demonstrating how to build responsible AI agents that orchestrate multiple data sources (Google Earth AI, FEMA NRI, BigQuery Earth Engine) while maintaining complete provenance tracking through Action Credentials and policy enforcement via OPA/Rego.

**Use Cases:**
- Insurance underwriters assessing hurricane risk
- Emergency planners evaluating wildfire scenarios
- Climate analysts comparing flood risk across regions

### Is this a commercial product?

**No.** TerraRisk Agent is a **personal R&D project** exploring the intersection of:
- AI agent frameworks (Google Earth AI, OpenAI AgentKit, Anthropic tool use)
- Geospatial intelligence (FEMA NRI, Earth Engine, satellite imagery)
- Responsible AI governance (A2PA, Sigstore, C2PA, OPA)

Treat it as a **reference implementation** and research platform—not production software.

### What makes TerraRisk Agent useful today?

**Even as a research platform, TerraRisk Agent demonstrates:**

1. **AI Agent Orchestration Patterns**: How to coordinate reasoning agents (Earth AI) with traditional data pipelines (BigQuery)
2. **Provenance-First Architecture**: Every decision is tracked with Action Credentials—showing how to build auditable AI systems
3. **Policy-Driven Security**: OPA policies enforce governance at runtime—demonstrating scalable AI agent deployments
4. **Production-Ready Infrastructure**: Sigstore signing, C2PA manifests, OpenTelemetry—all the pieces needed for regulated industries

**For Analysts:** Offline fixtures let you explore AI-powered geospatial analysis without cloud credentials.

**For Developers:** Reference implementation showing how to build trustworthy AI agents.

**For Security Professionals:** Demonstrates governance patterns for AI agent deployments.

### Who is the target audience?

**Primary Audiences:**

1. **Insurance Underwriters & Risk Analysts**: Exploring how AI can accelerate geospatial risk assessment
2. **Emergency Planners & Government Analysts**: Evaluating AI-powered scenario planning tools
3. **Technical Teams**: Building AI agent systems with provenance and governance
4. **Security & Governance Professionals**: Exploring policy enforcement and auditability patterns

**Secondary Audiences:**

- Climate researchers exploring AI-assisted geospatial analysis
- Students learning about responsible AI development
- Organizations evaluating AI agent frameworks

---

## Technical Questions

### How does TerraRisk Agent work?

**High-Level Flow:**

1. **User asks a question** in natural language (e.g., "Which Gulf Coast counties have the highest hurricane risk?")
2. **Planner agent decomposes** the query into geospatial analysis steps
3. **Connectors fetch data** from multiple sources (FEMA NRI, BigQuery Earth Engine, boundaries)
4. **Governance layer validates** each step through OPA policies
5. **Report generator produces** PDF, GeoJSON, and CSV artifacts with Action Credentials

**Technical Details:** See [`ARCHITECTURE.md`](ARCHITECTURE.md) for complete system design.

### What data sources does TerraRisk Agent use?

**Current Data Sources:**

1. **Google Earth AI** (stubbed): Geospatial reasoning agent that decomposes queries into executable steps
2. **FEMA National Risk Index**: Comprehensive hazard risk data at county level
3. **BigQuery Earth Engine**: Satellite imagery and geospatial analytics
4. **Boundary Data**: Geographic boundaries for visualization

**Modes:**

- **Offline**: Synthetic fixtures (no external dependencies)
- **BYO BigQuery**: Real BigQuery/Earth Engine (Earth AI stubbed)
- **Cloud**: Full integration (requires Earth AI API access)

### Can I use real customer data?

**Not by default.** The policy bundle enforces:
- **County-level granularity** (blocks street-level to prevent PII exposure)
- **PII safeguards** (requires explicit approval)
- **Budget limits** (prevents runaway costs)

**Before handling sensitive data:**

1. Review and extend OPA policies in `packages/policies/opa_bundle/policy.rego`
2. Update connectors to handle your data sources
3. Configure appropriate authentication and authorization
4. Audit Action Credential generation for compliance

**This is a research platform**—extend it responsibly before production use.

### How do I enable Earth AI once access opens?

**Steps:**

1. **Obtain API credentials** from Google's Earth AI program
2. **Set environment variable**: `EARTH_AI_ENABLED=1`
3. **Configure credentials** in `connectors/earth_ai.py` (replace stub implementation)
4. **Update OPA policies** to allow Earth AI actions for authorized roles
5. **Test in BYO BigQuery mode** first before full cloud deployment

**Current Status:** Earth AI API access is limited—TerraRisk Agent is ready for when access expands.

### What testing exists?

**Quality Assurance:**

1. **Unit Tests**: Cover analysis orchestration, report generation, connectors, API endpoints
   - Run: `cd apps/terrarisk-agent/backend && uv run pytest`

2. **Linting & Type Checking**: `ruff` for linting, `mypy` for type safety
   - Run: `uv run ruff check terrarisk && uv run mypy terrarisk`

3. **Frontend Tests**: Linting and build validation
   - Run: `cd frontend && pnpm lint && pnpm build`

4. **Evaluation Harness**: Golden Q&A with ROUGE-L F1 scoring
   - Run: `cd backend && uv run python ../evals/run_eval.py`
   - Target: ROUGE-L F1 ≥ 0.75, 100% join integrity

**All Checks:** `make qa` runs everything in one command.

---

## Governance & Security Questions

### How do we ensure outputs are trustworthy?

**Multiple Layers of Trust:**

1. **Action Credentials**: Every planner/report step emits an Action Credential tracking:
   - Inputs (what data was used)
   - Outputs (what was produced)
   - Source (who/what made the decision)
   - Timestamp (when it happened)

2. **Sigstore Signing**: Artifacts can be signed with Sigstore keyless signing:
   - No keys to manage (uses OIDC)
   - Rekor transparency log for public verification
   - Cryptographic proof of authenticity

3. **C2PA Manifests**: PDFs and images designed for C2PA (Content Credentials) manifests:
   - Embedded provenance metadata
   - Tamper detection
   - Verifiable authenticity

4. **Evaluation Gates**: Quality assurance via ROUGE-L F1 scoring and join integrity checks

**For Business Users:** Every report has a complete audit trail showing exactly what data was used and how decisions were made.

**For Technical Users:** Action Credentials follow A2PA schema, ready for Sigstore signing and C2PA binding.

### Does this integrate with policy or governance systems?

**Yes.** TerraRisk Agent demonstrates policy-driven governance through:

1. **OPA/Rego Bundles**: Deny-by-default enforcement with:
   - Feature flags (Earth AI enabled/disabled)
   - Budget limits (prevent runaway costs)
   - Geography granularity (county-level vs. street-level)
   - PII safeguards (requires explicit approval)

2. **Extensible Policies**: You can extend policies for:
   - Per-tool approvals (require approval before calling specific connectors)
   - Time-based restrictions (only allow analyses during business hours)
   - Data residency (ensure data stays within geographic boundaries)
   - Windows MCP mediation (integrate with Microsoft's Model Context Protocol)

**Policy Location:** `packages/policies/opa_bundle/policy.rego`

**How It Works:** OPA policies evaluate every action before execution. If a policy denies the action, the request fails with a 403 Forbidden response.

### How does observability work?

**Current Implementation:**

1. **OpenTelemetry SDK**: Hooks are ready for tracing
   - Traces export to local OTLP collector in docker-compose
   - Each analysis produces a trace with spans for planner, connectors, reports

2. **Action Credentials**: Provenance tracking embedded in every response
   - Track inputs, outputs, timestamps
   - Ready for correlation with traces

3. **Structured Logging**: Captures:
   - Analysis requests and responses
   - Policy decisions (allow/deny)
   - Connector execution (success/failure)
   - Report generation status

**Future Enhancements:**

- Thread trace IDs into Action Credentials for complete correlation
- Metrics dashboard (analysis latency, connector success rates, policy denials)
- Integration with observability platforms (Datadog, New Relic, etc.)

---

## Deployment Questions

### How do I run TerraRisk Agent?

**Easiest Way (No Code):**
```bash
cd ai-governance-suite
make demo-terra
```
Opens dashboard at http://localhost:3000 and API at http://localhost:8000/docs

**For Developers:** See [`QUICKSTART.md`](QUICKSTART.md) for detailed setup instructions.

**For Production:** This is a research platform—extend responsibly before production deployment.

### What are the system requirements?

**Minimum Requirements:**

- **Docker Desktop** (for demo mode)
- **Python 3.11+** (for development)
- **Node.js 20+** (for frontend development)
- **4GB RAM** (for running containers)

**Recommended:**

- **Devcontainer** (VS Code or GitHub Codespaces): Everything pre-configured
- **8GB RAM**: For comfortable development experience
- **Google Cloud credentials**: For BYO BigQuery or Cloud modes

### Where can I contribute?

**Contributions Welcome:**

1. **New Connectors**: Add data sources (NOAA, USGS, etc.)
2. **Policy Extensions**: Enhance OPA policies for new use cases
3. **Evaluation Fixtures**: Add golden Q&A examples
4. **Documentation**: Improve clarity and examples

**Process:**

1. See [`QUICKSTART.md`](QUICKSTART.md) for setup
2. Review [`ARCHITECTURE.md`](ARCHITECTURE.md) to understand modules
3. Open pull requests with improvements

**Note:** This is a personal R&D project—contributions should align with the research goals of exploring responsible AI agent development.

---

## Data & Provenance Questions

### What data sources are included offline?

**Offline Fixtures:**

1. **Synthetic FEMA NRI**: Sample county-level risk data for hurricane/flood hazards
   - Location: `apps/terrarisk-agent/backend/terrarisk/examples/offline_nri.csv`
   - Format: CSV with county FIPS, hazard types, EAL (Expected Annual Loss), resilience index

2. **Placeholder Boundaries**: GeoJSON for county boundaries
   - Compatible with MapLibre for visualization

3. **MapLibre Basemap References**: Public tile servers for map display

**Note:** Offline fixtures are simplified and should not be used for real underwriting decisions.

### How does provenance tracking work?

**Action Credentials Track:**

- **Inputs**: What data sources were queried
- **Outputs**: What artifacts were generated
- **Source**: Which system/component made the decision
- **Timestamp**: When the action occurred
- **Artifacts**: References to generated files with hashes

**Example:**
```json
{
  "id": "cred-abc123",
  "action": {
    "type": "planner.step.nri_loader",
    "source": {"system": "nri_loader", "version": "1.0.0"}
  },
  "inputs": ["22071", "12086"],
  "outputs": ["nri-data-xyz"],
  "artifacts": [
    {"uri": ".../report.pdf", "type": "application/pdf", "hash": "sha256:..."}
  ],
  "timestamp": "2024-01-15T10:30:00Z"
}
```

**Use Cases:**
- Audit compliance: "Show me the decision trail"
- Reproducibility: "Can we run this exact analysis again?"
- Trust: "Verify this report hasn't been tampered with"

---

## Limitations & Future Work

### What are the current limitations?

**Known Limitations:**

1. **Earth AI is Stubbed**: Real Google Earth AI integration awaits API access
2. **PDFs are Placeholder**: Production should use WeasyPrint templates with C2PA manifests
3. **Deterministic Planner**: Will incorporate dynamic reasoning once Earth AI is available
4. **No Persistence**: Postgres in docker-compose is reserved for future stateful scenarios
5. **Offline Fixtures Simplified**: Not suitable for real underwriting decisions

**These are intentional**—TerraRisk Agent prioritizes demonstrating architecture patterns over production completeness.

### What's on the roadmap?

**Near-Term:**

- Real Earth AI client integration (when API access is available)
- Enhanced PDF generation with C2PA 2.2 manifests
- BigQuery DataFrames for analytics
- Expanded mitigation playbooks

**Long-Term:**

- Windows MCP mediation support
- Multi-agent orchestration patterns
- Advanced evaluation metrics
- Production deployment guides

---

## Getting Help

### Where do I find more information?

**Documentation:**

- [`QUICKSTART.md`](QUICKSTART.md): Getting started guide
- [`ARCHITECTURE.md`](ARCHITECTURE.md): System design deep dive
- [`API_REFERENCE.md`](API_REFERENCE.md): Complete API documentation
- [`APPENDICES.md`](APPENDICES.md): Reference materials

**Code:**

- `apps/terrarisk-agent/backend/`: Backend implementation
- `apps/terrarisk-agent/frontend/`: Frontend implementation
- `packages/policies/`: OPA policy bundles
- `packages/schemas/`: Action Credential schemas

### How do I report issues?

**This is a research platform**—issues are expected as we explore new patterns. Check the codebase first—it's well-commented and designed for learning.

---

## Key Takeaways

**For Business Users:**
- TerraRisk Agent demonstrates how AI can accelerate geospatial risk analysis
- Every output is auditable and verifiable
- Offline mode lets you explore without cloud credentials

**For Technical Users:**
- Reference implementation for building responsible AI agents
- Demonstrates provenance tracking, policy enforcement, and observability
- Modern stack (FastAPI, Next.js, OpenTelemetry) ready for extension

**For Security Professionals:**
- Policy-driven governance with OPA/Rego
- Action Credentials for complete audit trails
- Sigstore and C2PA integration ready

---

**Have a question not covered here?** Check the other documentation files or explore the codebase—it's designed to be readable and educational.
