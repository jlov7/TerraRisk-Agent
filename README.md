# AI Governance Suite: Building Trustworthy AI Agents for Real-World Impact

> **What if AI agents could help us understand climate risks, make better decisions, and do it all while maintaining complete transparency and accountability?** This is the question that drives the AI Governance Suite—a research platform exploring how to build AI agents that are not just powerful, but also responsible, auditable, and ready for mission-critical applications.

## The Vision: AI Agents We Can Trust

In an era where AI agents are revolutionizing everything from customer service to scientific research, we face a critical challenge: **how do we ensure these agents make decisions we can verify, audit, and trust?** 

The AI Governance Suite explores this frontier through **TerraRisk Agent**, a geospatial intelligence copilot that demonstrates how modern AI agents can:

- **Reason about complex geospatial problems** using Google Earth AI's advanced capabilities
- **Orchestrate multiple data sources** (FEMA National Risk Index, BigQuery Earth Engine, satellite imagery)
- **Produce auditable, signed outputs** with complete provenance tracking
- **Enforce policies and governance** at every step through Open Policy Agent (OPA)

## Why This Matters Today

### The AI Agent Revolution
We're witnessing an explosion of AI agent frameworks—OpenAI's AgentKit, Microsoft's Agent Framework, Anthropic's tool use models, and Google's Earth AI. These agents can reason, plan, and execute complex workflows. But **who's responsible when an AI agent makes a decision?** How do you audit a multi-step reasoning process? How do you prove a report wasn't tampered with?

### Geospatial Intelligence Meets Climate Risk
Climate change is reshaping our world. Insurance companies need to assess risk faster. Emergency planners need actionable insights. Governments need evidence-based policies. Traditional geospatial analysis is slow and requires deep expertise. **AI agents can accelerate this by orders of magnitude**—but only if we can trust their outputs.

### The Compliance Imperative
As AI agents enter regulated industries (insurance, finance, healthcare, government), they must comply with:
- **Audit requirements** (who made what decision, when, and why?)
- **Data governance** (where did the data come from? Is it authoritative?)
- **Security policies** (what actions are allowed? What's the budget?)
- **Provenance tracking** (can we reproduce this analysis? Can we verify it wasn't modified?)

## What You'll Find Here

### 🌍 TerraRisk Agent: The Flagship Example
A complete implementation demonstrating how to build a geospatial underwriting copilot that:
- Decomposes complex natural language queries into executable geospatial workflows
- Integrates Google Earth AI reasoning, FEMA risk data, and BigQuery Earth Engine analytics
- Produces signed, provenance-tracked reports with PDF, GeoJSON, and CSV artifacts
- Enforces governance policies through OPA/Rego bundles

**Perfect for:** Insurance underwriters, emergency planners, climate risk analysts, or anyone exploring how AI agents can transform geospatial intelligence.

### 🔐 Governance & Compliance Framework
- **Action Credentials**: A2PA-aligned schema for tracking every AI decision
- **OPA Policies**: Deny-by-default enforcement with budget limits, PII safeguards, and feature flags
- **Sigstore Integration**: Keyless signing ready for production deployment
- **C2PA Support**: Content credentials for media artifacts (PDFs, images)

### 🧪 Evaluation & Quality Assurance
- Golden Q&A evaluation harness
- ROUGE-L F1 scoring for narrative quality
- Join integrity validation
- Reproducible artifact checksums

## Quick Start

**For Business Stakeholders / Analysts:**
```bash
cd ai-governance-suite
make demo-terra
# Open http://localhost:3000 - explore the dashboard
# Open http://localhost:8000/docs - explore the API
```

**For Developers:**
```bash
# Use the devcontainer (VS Code / GitHub Codespaces)
# Everything is pre-configured: Python, Node, OPA, Sigstore tools

# Or run locally:
cd apps/terrarisk-agent/backend
uv run uvicorn terrarisk.main:app --reload

cd ../frontend
pnpm install && pnpm dev
```

See [`docs/QUICKSTART.md`](docs/QUICKSTART.md) for detailed setup instructions.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    User Query (Natural Language)            │
│          "Which Gulf Coast counties have highest            │
│           hurricane risk this quarter?"                      │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                    Planner Agent                            │
│  • Decomposes query into geospatial steps                   │
│  • Orchestrates Earth AI reasoning + data joins             │
│  • Builds execution graph                                   │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                    Connectors Layer                         │
│  • Earth AI (Google's geospatial reasoning)                 │
│  • FEMA National Risk Index                                 │
│  • BigQuery Earth Engine                                    │
│  • Boundary providers                                       │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                    Governance Layer                         │
│  • OPA policies enforce budgets, approvals                  │
│  • Action credentials track every step                      │
│  • Provenance metadata captured                             │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                    Report Generation                        │
│  • PDF reports with mitigation recommendations              │
│  • GeoJSON layers for visualization                         │
│  • CSV portfolio analyses                                   │
│  • Signed artifacts with C2PA manifests                     │
└─────────────────────────────────────────────────────────────┘
```

## Project Structure

```
ai-governance-suite/
├── apps/
│   └── terrarisk-agent/          # Complete TerraRisk Agent implementation
│       ├── backend/               # FastAPI service with planner, connectors, reports
│       ├── frontend/              # Next.js dashboard with map visualization
│       └── evals/                 # Evaluation harness and golden Q&A
├── packages/
│   ├── schemas/                   # Action Credential schemas (A2PA-aligned)
│   ├── policies/                  # OPA/Rego policy bundles
│   └── otel/                      # OpenTelemetry configuration
└── docs/                          # Comprehensive documentation
    ├── ARCHITECTURE.md            # Deep dive into system design
    ├── QUICKSTART.md              # Getting started guide
    ├── API_REFERENCE.md           # API endpoint documentation
    ├── FAQ.md                     # Common questions
    └── APPENDICES.md              # Reference materials
```

## Key Features

### 🔄 Three Operational Modes
1. **Offline Mode** (default): Synthetic fixtures—perfect for demos without cloud credentials
2. **BYO BigQuery**: Use your own BigQuery/Earth Engine—Earth AI remains stubbed until access is available
3. **Cloud Mode**: Full integration with Earth AI + BigQuery—requires API access

### 🛡️ Built-in Governance
- **Policy Enforcement**: Deny-by-default with OPA/Rego bundles
- **Budget Controls**: Prevent runaway API costs
- **PII Safeguards**: County-level granularity by default
- **Feature Flags**: Control access to experimental capabilities

### 📊 Complete Observability
- OpenTelemetry traces for every analysis
- Action credentials for every decision
- Reproducible artifact checksums
- Evaluation gates for quality assurance

## Use Cases

### For Insurance Underwriters
*"I need to assess hurricane risk for a portfolio of properties along the Gulf Coast. Generate a report with risk rankings, mitigation recommendations, and portfolio-level stress metrics."*

TerraRisk Agent can:
- Parse your natural language query
- Decompose it into geospatial analysis steps
- Pull FEMA NRI data, satellite imagery, and historical patterns
- Generate an auditable report with signed artifacts

### For Emergency Planners
*"What's the wildfire risk scenario for California's Central Valley this quarter? What actions should we prioritize?"*

TerraRisk Agent can:
- Generate scenario-based analyses
- Rank hazards by severity and exposure
- Recommend mitigation actions
- Provide reproducible, verifiable outputs

### For Climate Risk Analysts
*"Compare flood risk across three different regions and produce a comparative analysis with visualizations."*

TerraRisk Agent can:
- Join multiple data sources
- Generate comparative visualizations
- Create signed reports with complete provenance

## The Technical Journey

### For Technical Readers
This suite demonstrates:
- **Multi-agent orchestration**: How to coordinate reasoning agents (Earth AI) with data connectors (BigQuery, FEMA)
- **Provenance tracking**: Action Credentials following A2PA standards, ready for Sigstore signing
- **Policy-driven governance**: OPA/Rego bundles enforcing security, budget, and compliance policies
- **Modern AI stack**: FastAPI, Next.js, OpenTelemetry, containerized deployment

### For Business Readers
Think of TerraRisk Agent as a **trusted AI assistant**:
- You ask questions in plain language
- It figures out what data sources to consult
- It performs complex geospatial analysis
- It produces reports you can verify and audit
- Every step is tracked and can be signed

## Why This Is Cutting-Edge

### 1. **Agent Orchestration at Scale**
Combines multiple AI reasoning engines (Earth AI) with traditional data pipelines (BigQuery) in a unified workflow.

### 2. **Provenance-First Architecture**
Every decision is tracked with Action Credentials—demonstrating how to build auditable AI systems.

### 3. **Policy-Driven Security**
OPA policies enforce governance at runtime—showing how to scale AI agent deployments safely.

### 4. **Production-Ready Patterns**
Sigstore signing, C2PA manifests, OpenTelemetry—all the infrastructure needed for regulated industries.

## What's Next?

This is a **research platform**—a sandbox for exploring responsible AI agent development. Current roadmap:
- ✅ Multi-agent orchestration patterns
- ✅ Action Credential provenance tracking
- ✅ OPA policy enforcement
- 🔄 Real Earth AI integration (when API access is available)
- 🔄 Enhanced BigQuery DataFrames integration
- 🔄 Expanded mitigation playbooks
- 🔄 Windows MCP mediation support

## Contributing & Research

This is a **personal R&D project** exploring the intersection of:
- AI agent frameworks (Google Earth AI, OpenAI AgentKit, Anthropic tool use)
- Geospatial intelligence (FEMA NRI, Earth Engine, satellite imagery)
- Responsible AI governance (A2PA, Sigstore, C2PA, OPA)

**Not a commercial product**—treat it as a reference implementation and research platform.

## Documentation

- **[Architecture Deep Dive](docs/ARCHITECTURE.md)**: How the pieces fit together
- **[Quickstart Guide](docs/QUICKSTART.md)**: Get up and running in minutes
- **[API Reference](docs/API_REFERENCE.md)**: Complete endpoint documentation
- **[FAQ](docs/FAQ.md)**: Common questions answered
- **[TerraRisk Agent README](apps/terrarisk-agent/README.md)**: Application-specific details

## References & Inspiration

- [Google Earth AI](https://blog.google/technology/ai/google-earth-ai-oct-2023/) - Geospatial reasoning agents
- [FEMA National Risk Index](https://hazards.fema.gov/nri/learn-more) - Comprehensive hazard data
- [Sigstore](https://docs.sigstore.dev/) - Keyless signing for software supply chain
- [C2PA](https://c2pa.org/specifications/specifications) - Content Credentials for media provenance
- [Open Policy Agent](https://www.openpolicyagent.org/) - Policy-as-code enforcement

---

**Built with curiosity. Designed for accountability. Ready for the future of AI.**
