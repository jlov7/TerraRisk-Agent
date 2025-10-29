# TerraRisk Agent FAQ

### Is this a commercial product?
No. TerraRisk Agent is a personal passion R&D project to explore geospatial underwriting workflows and responsible AI provenance. Treat it as a sandbox, not production software.

### What makes it useful today?
- Demonstrates how a geospatial reasoning agent could orchestrate Earth AI, FEMA NRI, and BigQuery Earth Engine.
- Provides offline fixtures so analysts can experiment without cloud credentials.
- Ships with provenance tooling (Action Credentials, C2PA-ready artifacts) to showcase trusted AI outputs.

### Can I use real customer data?
Not by default. The policy bundle enforces county-level granularity and blocks PII unless explicitly approved. Extend the connectors and policies before handling sensitive data.

### How do we enable Earth AI once access opens?
1. Obtain API credentials from Google’s Earth AI program.
2. Set `EARTH_AI_ENABLED=1` and configure the real client in `connectors/earth_ai.py`.
3. Update OPA policies to allow the Earth AI action for authorized roles.

### What data sources are included offline?
- Synthetic FEMA National Risk Index slice (a few counties for hurricane/flood hazards).
- Placeholder boundary geometries.
- MapLibre basemap references (public tiles).

### How do we ensure outputs are trustworthy?
- Each planner/report step emits an `ActionCredential` referencing inputs, outputs, provenance, and hashes.
- Artifacts can be signed with Sigstore (keyless) and bound with C2PA manifests when realistic assets are produced.
- Evaluation harness enforces minimum narrative quality (ROUGE-L F1) and verifies join integrity on fixtures.

### Does this integrate with policy or governance systems?
Yes. The OPA/Rego bundle demonstrates deny-by-default enforcement, feature flags, budget limits, and PII safeguards. You can extend it to include per-request approvals, tool allowlists, or Windows MCP mediation.

### How does observability work?
- OTEL SDK hooks are ready; traces export to the local OTLP collector in docker-compose.
- Trace IDs will be threaded into action credentials (future improvement) to correlate analytics and provenance.

### What testing exists?
- Unit tests cover analysis orchestration, report generation, Earth AI stubs, and API endpoints.
- Linting (`ruff`), type checking (`mypy`), and frontend lint/build commands keep code quality high.
- Eval harness (`evals/run_eval.py`) provides narrative accuracy checks against golden questions.

### Where do I contribute?
- See `docs/QUICKSTART.md` for setup.
- Review `docs/ARCHITECTURE.md` to understand modules.
- Open pull requests with new connectors, policies, or evaluation fixtures to keep the demo evolving.

### Who is the audience?
- Underwriters and emergency planners seeking a taste of geospatial copilots.
- Technical teams evaluating provenance-aware agent stacks.
- Governance/security stakeholders exploring how to bind AI outputs with signed credentials.
