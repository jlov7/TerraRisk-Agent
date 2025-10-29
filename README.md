# AI Governance Suite (Personal R&D)

This monorepo explores compliance-aware agentic workflows. TerraRisk Agent is the newest addition, focusing on geospatial underwriting using Google Earth AI inspiration, FEMA NRI, and BigQuery Earth Engine templates.

## Layout
- `apps/terrarisk-agent` – FastAPI backend, Next.js frontend, eval harness, and examples.
- `packages/schemas` – Shared schemas such as Action Credentials (A2PA-aligned).
- `packages/policies` – OPA/Rego bundles enforcing deny-by-default and per-tool approvals.
- `packages/otel` – OpenTelemetry collector settings.
- `docs/` – Quickstart, architecture notes, API reference, FAQ, and shared appendices.

## Tooling
- `devcontainer.json` preloads uv, ruff, mypy, cosign, opa, Node/pnpm, and Go.
- `docker-compose.yml` runs Postgres, Redis, OPA, OTEL collector, and the TerraRisk services.
- `Makefile` exposes `make dev`, `make demo-terra`, and placeholders for seed/test/chaos flows.

> Personal R&D disclaimer: nothing here is a commercial product; it is a sandbox for experimenting with policy-aligned AI agents.
