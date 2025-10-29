# Appendices

## 1. Action Credential (A2PA)
- Schema: `packages/schemas/action_credential_v0.json`
- Signing: Sigstore keyless (cosign) with in-toto attestations; store Rekor URLs / OCI references.
- Media outputs should embed C2PA 2.2 manifests where supported; otherwise capture soft bindings with SHA-256 fingerprints.

## 2. OPA/Rego Policy Bundle
- Primary policy: `packages/policies/opa_bundle/policy.rego`
- Deny by default, enforce Earth AI feature flagging, budget quotas, and PII scope approvals.
- Extend inputs to model Windows MCP per-tool approvals and proxy mediation.

## 3. Devcontainer & Compose
- Devcontainer preloads uv, ruff, mypy, cosign, opa, Node/pnpm, and Go toolchains.
- `docker-compose.yml` starts Postgres, Redis, OPA, OTEL collector, backend, and frontend for consistent demos.

## 4. CI (GitHub Actions)
- Intended pipeline: lint/type/test → build images → SBOM → cosign sign (OIDC, keyless) → push to GHCR → publish docs.
- Example OIDC ↔ cosign flow uses ambient identity (no static secrets).

## 5. Eval Gates
- TerraRisk Agent target: offline ROUGE-L F1 ≥ 0.75, join-integrity 100% on fixtures, reproducible artifact hashes per run.
- Copy this gate into service READMEs to keep quality guardrails visible.
