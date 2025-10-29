# TerraRisk Agent Architecture

TerraRisk Agent is a personal R&D exploration of a geospatial underwriting copilot. This document explains how the pieces fit together for both technical and non-technical readers.

## High-level story
1. A user (analyst, emergency planner, underwriter) asks a multi-step question.
2. The planner decomposes the request into geospatial steps, alternating between Earth AI reasoning (stub today) and data joins.
3. Connectors fetch/aggregate data (NRI fixtures offline, BigQuery/Earth Engine in cloud mode).
4. The report composer bundles artifacts (PDF, GeoJSON, CSV) and records provenance.
5. Action credentials capture who/what/when so outputs remain auditable and signable.

## Core components

| Layer | What it does | Key files |
| --- | --- | --- |
| API | FastAPI service exposing health, analysis, scenarios, portfolio stress endpoints. | `backend/terrarisk/main.py` |
| Planner | Builds a step graph combining Earth AI plan suggestions with hazard + portfolio operations. | `backend/terrarisk/agents/planner.py` |
| Connectors | Modular data clients for Earth AI (stub/real), BigQuery Earth Engine, FEMA NRI, Data Commons, boundaries. | `backend/terrarisk/connectors/*.py` |
| Services | Orchestrates planner output, executes joins, ranks hazards, and generates deliverables. | `backend/terrarisk/services/analysis.py` |
| Reports | Creates PDFs, GeoJSON, CSV artifacts, and action credentials (provenance). | `backend/terrarisk/reports/compose.py` |
| Frontend | Next.js dashboard with map preview and artifact downloads. | `frontend/app/page.tsx`, `frontend/components/MapPreview.tsx` |
| Eval Harness | Golden Q&A + crisis fixtures to track narrative quality and join integrity. | `evals/run_eval.py`, `evals/golden_qa.jsonl` |

## Modes of operation
- **Offline** (default): Synthetic fixtures stand in for Earth AI and FEMA NRI data. Perfect for demos without external dependencies.
- **BYO BigQuery**: You bring GCP credentials—Earth AI remains stubbed—but BigQuery/Earth Engine queries execute for your assets.
- **Cloud**: Earth AI API + BigQuery/Earth Engine combined. Feature-flagged with `EARTH_AI_ENABLED=1`.

## Data provenance
- Every planner step and report action emits an `ActionCredential` (see `packages/schemas/action_credential_v0.json`).
- Signatures are ready for Sigstore and C2PA binding once real artifacts are produced.
- OTEL spans (future work) will thread trace IDs into every credential.

## Security posture (R&D commitments)
- Least-privilege principle in infrastructure (service accounts, OPA policies).
- Deny-by-default OPA bundle gating Earth AI usage, budget, and PII scope.
- SBOM + cosign signing in the GitHub Actions pipeline (stubbed for now; config provided in `.github/workflows/ci.yml`).

## Developer experience
- Devcontainer (VS Code / Codespaces) with all required CLIs (uv, ruff, mypy, cosign, opa, Node, Go).
- Make targets for local dev, tests, chaos experiments (future).
- docker-compose orchestrates Postgres, Redis, OPA, OTEL collector, backend, frontend.

## Extension points
- Replace `EarthAIStubClient` with real API calls when access opens.
- Swap `NRILoader` to point at FEMA tables or Data Commons connectors.
- Add new hazard scenarios by extending `ScenarioResponse` logic and hooking in the planner.
- Integrate Microsoft Agent Framework, OpenAI AgentKit, or Mistral Agents via adapters (future packages).

## Limitations (today)
- Offline fixtures are simplified and should not be used for real underwriting decisions.
- PDF generation is placeholder text; production build should render with WeasyPrint templates and embed C2PA manifests.
- Planner logic is deterministic; once Earth AI is available, incorporate dynamic reasoning outputs.
- No persistence layer yet; Postgres in docker-compose is reserved for future stateful scenarios.

This architecture intentionally keeps complexity manageable while leaving hooks for enterprise-grade provenance, evaluation, and policy enforcement. Use it as a blueprint to experiment, validate assumptions, and iterate as access to Earth AI expands.
