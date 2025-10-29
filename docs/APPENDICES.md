# Appendices: Reference Materials

Technical reference materials for TerraRisk Agent. This document provides detailed information about schemas, policies, infrastructure, and evaluation criteria.

---

## 1. Action Credential Schema (A2PA-Aligned)

### Overview

**Action Credentials** are the building blocks of provenance tracking in TerraRisk Agent. They follow the **AI Agent Provenance Architecture (A2PA)** schema, designed to be auditable, signable, and verifiable.

### What Are Action Credentials?

Think of Action Credentials as **digital receipts** for AI decisions:
- **Who/What**: Which system made the decision
- **When**: Timestamp of the action
- **Inputs**: What data was used
- **Outputs**: What was produced
- **Artifacts**: References to generated files

### Schema Location

**File:** `packages/schemas/action_credential_v0.json`

### Schema Structure

```json
{
  "id": "unique-credential-id",
  "action": {
    "type": "planner.step.{source}",
    "source": {
      "system": "system-identifier",
      "version": "1.0.0"
    }
  },
  "inputs": ["input1", "input2"],
  "outputs": ["output1"],
  "artifacts": [
    {
      "uri": "file:///path/to/artifact.pdf",
      "type": "application/pdf",
      "hash": "sha256:abc123..."
    }
  ],
  "claims": [
    {"name": "description", "value": "Human-readable description"}
  ],
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Signing & Verification

**Sigstore Keyless Signing:**

```bash
# Sign an Action Credential
cosign sign-blob --yes credential.json

# Verify signature
cosign verify-blob credential.json
```

**Benefits:**
- No keys to manage (uses OIDC authentication)
- Rekor transparency log for public verification
- Cryptographic proof of authenticity

### C2PA Integration

**For Media Artifacts (PDFs, Images):**

- Embed C2PA 2.2 manifests in generated PDFs
- Capture soft bindings with SHA-256 fingerprints for non-C2PA-compatible formats
- Link Action Credentials to C2PA manifests via artifact URIs

**Example Workflow:**
1. Generate PDF with C2PA manifest
2. Create Action Credential referencing PDF URI
3. Sign Action Credential with Sigstore
4. Verify both PDF and credential independently

### Use Cases

**For Compliance:**
- Audit trails: "Show me all decisions made by this system"
- Reproducibility: "Can we run this exact analysis again?"
- Verification: "Prove this report hasn't been tampered with"

**For Integration:**
- Chain multiple analyses together
- Track dependencies between analyses
- Build provenance graphs

---

## 2. OPA/Rego Policy Bundle

### Overview

**Open Policy Agent (OPA)** is a policy engine that enforces governance rules at runtime. TerraRisk Agent uses OPA/Rego bundles to implement **deny-by-default** security and policy enforcement.

### What Are OPA Policies?

Think of OPA policies as **automated compliance officers**:
- **Evaluate every action** before it executes
- **Enforce rules** like budget limits, feature flags, geography restrictions
- **Deny by default**—everything is blocked unless explicitly allowed

### Policy Location

**File:** `packages/policies/opa_bundle/policy.rego`

### Policy Structure

```rego
package terrarisk

# Default deny
default allow_earth_ai = false

# Allow Earth AI if feature flag is enabled and user has permission
allow_earth_ai {
    input.feature_flags.earth_ai_enabled == true
    input.user.role == "analyst"
}

# Enforce budget limits
deny {
    input.analysis.cost_estimate > input.user.budget_limit
}

# Block PII access (street-level geographies)
deny {
    input.analysis.geography_granularity == "street"
    not input.user.pii_approved
}
```

### Policy Enforcement Points

**When Policies Are Evaluated:**

1. **Before Earth AI calls**: Check if Earth AI is enabled for this user/role
2. **Before BigQuery queries**: Verify budget limits and geography restrictions
3. **Before report generation**: Validate artifact permissions

**How It Works:**

1. TerraRisk Agent sends context to OPA server
2. OPA evaluates policies and returns allow/deny decision
3. If denied, TerraRisk Agent returns 403 Forbidden with explanation

### Extending Policies

**Common Extensions:**

1. **Per-Tool Approvals:**
```rego
allow_bigquery {
    input.tool == "bigquery"
    input.user.approved_tools[_] == "bigquery"
}
```

2. **Time-Based Restrictions:**
```rego
deny {
    input.tool == "earth_ai"
    hour := time.clock(input.timestamp)[0]
    hour < 9  # Only allow during business hours
    hour > 17
}
```

3. **Data Residency:**
```rego
deny {
    input.dataset.region != "us-east1"
    input.user.data_residency == "us-only"
}
```

4. **Windows MCP Mediation:**
```rego
allow_action {
    input.mcp_approval == true
    input.action in input.mcp_allowlist
}
```

### Testing Policies

**Use OPA CLI:**
```bash
# Test a policy
opa test packages/policies/opa_bundle/policy.rego

# Evaluate with input
opa eval --data packages/policies/opa_bundle/policy.rego \
  --input input.json \
  'data.terrarisk.allow_earth_ai'
```

---

## 3. Devcontainer & Docker Compose

### Devcontainer Configuration

**What It Provides:**

- **Python 3.11+** with `uv` package manager
- **Node.js 20+** with `pnpm`
- **Development Tools**: `ruff`, `mypy`, `cosign`, `opa`
- **Go Toolchain**: For OPA policy development

**How to Use:**

1. Open in VS Code or GitHub Codespaces
2. VS Code prompts: "Reopen in Container"
3. Wait for container to build (~5 minutes first time)
4. Everything is pre-configured and working

**Benefits:**
- Zero setup friction
- Consistent development environment
- No "works on my machine" issues

### Docker Compose Services

**Services Started by `make demo-terra`:**

| Service | Purpose | Port |
|---------|---------|------|
| **PostgreSQL** | Future stateful scenarios | 5432 |
| **Redis** | Caching layer | 6379 |
| **OPA Server** | Policy enforcement | 8181 |
| **OpenTelemetry Collector** | Observability | 4317, 4318 |
| **Backend** | FastAPI service | 8000 |
| **Frontend** | Next.js dashboard | 3000 |

**Configuration:**
- `docker-compose.yml`: Service definitions
- Environment variables: Configured via `.env` files
- Networking: All services on same Docker network

**Starting Services:**
```bash
# Start all services
make demo-terra

# Start specific services
docker-compose up -d postgres redis opa

# View logs
docker-compose logs -f backend
```

---

## 4. CI/CD Pipeline (GitHub Actions)

### Intended Pipeline Flow

**Current Status:** CI configuration is provided but stubbed for now.

**Intended Flow:**

1. **Lint & Type Check**
   - `ruff check`: Python linting
   - `mypy`: Type checking
   - `pnpm lint`: Frontend linting

2. **Tests**
   - `pytest`: Backend unit tests
   - `pnpm test`: Frontend tests (future)

3. **Evaluation Gate**
   - `run_eval.py`: ROUGE-L F1 ≥ 0.75
   - Join integrity: 100%

4. **Build Images**
   - Build backend Docker image
   - Build frontend Docker image

5. **SBOM Generation**
   - Generate Software Bill of Materials
   - Track dependencies for security audits

6. **Sign with Sigstore**
   - Keyless signing using OIDC
   - Push signed images to GHCR (GitHub Container Registry)

7. **Publish Documentation**
   - Build documentation site
   - Deploy to GitHub Pages

### OIDC ↔ Cosign Flow

**Keyless Signing:**

```yaml
# Example GitHub Actions workflow
- name: Sign with Cosign
  uses: sigstore/cosign-installer@v3
- name: Sign image
  run: |
    cosign sign --yes \
      --oidc-issuer https://token.actions.githubusercontent.com \
      --identity-token ${{ steps.oidc-token.outputs.token }} \
      ghcr.io/user/terrarisk-agent:${{ github.sha }}
```

**Benefits:**
- No static secrets (uses ambient identity)
- Rekor transparency log
- Verifiable signatures

---

## 5. Evaluation Gates

### Quality Assurance Criteria

**TerraRisk Agent Target Metrics:**

| Metric | Target | Purpose |
|--------|--------|---------|
| **ROUGE-L F1** | ≥ 0.75 | Narrative quality (how well summaries match expected outputs) |
| **Join Integrity** | 100% | Data correctness (ensures geospatial joins are accurate) |
| **Reproducibility** | 100% | Artifact checksums match for identical inputs |

### ROUGE-L F1 Scoring

**What It Measures:**
- How well generated summaries match expected "golden" summaries
- Uses longest common subsequence (LCS) matching
- F1 score balances precision and recall

**How to Run:**
```bash
cd apps/terrarisk-agent/backend
uv run python ../evals/run_eval.py
```

**Golden Q&A Location:**
- `apps/terrarisk-agent/evals/golden_qa.jsonl`

**Format:**
```jsonl
{"query": "Which Gulf Coast counties have highest hurricane risk?", "expected_summary": "Expected narrative here..."}
{"query": "What's the wildfire risk for California?", "expected_summary": "..."}
```

### Join Integrity Checks

**What It Measures:**
- Ensures geospatial data joins are correct
- Validates county FIPS codes match boundaries
- Verifies hazard data aligns with geography filters

**How It Works:**
1. Load test fixtures
2. Run analysis
3. Verify joins match expected results
4. Report integrity percentage

### Reproducibility Checks

**What It Measures:**
- Same inputs produce identical outputs
- Artifact checksums match across runs
- Deterministic execution

**How to Verify:**
```bash
# Run analysis twice with same inputs
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"query": "test", "mode": "offline"}' > run1.json

curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"query": "test", "mode": "offline"}' > run2.json

# Compare artifact hashes
jq '.artifacts[].hash' run1.json run2.json
```

### Evaluation Gate in CI

**GitHub Actions Example:**
```yaml
- name: Run evaluation gate
  run: |
    cd apps/terrarisk-agent/backend
    uv run python ../evals/run_eval.py
    # Fails if ROUGE-L F1 < 0.75 or join integrity < 100%
```

**Purpose:** Prevent regressions in narrative quality and data correctness.

---

## 6. BigQuery Earth Engine SQL Templates

### Example Queries

**Hurricane Wind Analysis:**
```sql
SELECT
  county_fips,
  stats.mean_wind_speed,
  stats.max_wind_speed
FROM ST_REGIONSTATS(
  (
    SELECT geom, county_fips 
    FROM `project.dataset.county_boundaries`
    WHERE county_fips IN ('22071', '12086')
  ),
  (
    SELECT * 
    FROM `project.dataset.noaa_hurricane_wind`
    WHERE timestamp >= TIMESTAMP('2024-01-01')
  ),
  STRUCT(
    sample_size => 500,
    reducer => 'MEAN'
  )
);
```

**Flood Risk Aggregation:**
```sql
SELECT
  county_fips,
  AVG(flood_depth) as avg_flood_depth,
  MAX(flood_depth) as max_flood_depth
FROM `project.dataset.flood_risk`
WHERE county_fips IN ('22071', '12086')
GROUP BY county_fips;
```

### Template Location

**Future:** Template queries will be stored in `backend/terrarisk/connectors/bigquery_ee.py` for reuse.

---

## 7. OpenTelemetry Configuration

### Collector Config

**File:** `packages/otel/collector-config.yml`

### Current Configuration

- **OTLP Receiver**: Receives traces from TerraRisk Agent
- **OTLP Exporter**: Exports to observability backend (future)
- **Logging Exporter**: Logs traces for debugging

### Future Enhancements

- **Metrics Export**: Analysis latency, connector success rates
- **Trace Sampling**: Sample traces based on query type
- **Backend Integration**: Export to Datadog, New Relic, etc.

---

## 8. Reference Links

### Standards & Specifications

- **A2PA**: AI Agent Provenance Architecture (in development)
- **Sigstore**: [Keyless signing documentation](https://docs.sigstore.dev/)
- **C2PA**: [Content Credentials 2.2 specification](https://c2pa.org/specifications/specifications)
- **OPA**: [Open Policy Agent documentation](https://www.openpolicyagent.org/)
- **OpenTelemetry**: [OTEL specification](https://opentelemetry.io/docs/)

### Data Sources

- **Google Earth AI**: [Blog post](https://blog.google/technology/ai/google-earth-ai-oct-2023/)
- **FEMA NRI**: [National Risk Index](https://hazards.fema.gov/nri/learn-more)
- **BigQuery Earth Engine**: [Documentation](https://cloud.google.com/bigquery/docs/geospatial)

### Tools

- **FastAPI**: [Documentation](https://fastapi.tiangolo.com/)
- **Next.js**: [Documentation](https://nextjs.org/docs)
- **MapLibre**: [Documentation](https://maplibre.org/)

---

## Summary

These appendices provide the technical foundation for TerraRisk Agent:

- **Action Credentials**: Provenance tracking with Sigstore/C2PA integration
- **OPA Policies**: Policy-driven governance and security
- **Infrastructure**: Devcontainer, Docker Compose, CI/CD
- **Evaluation**: Quality gates for narrative quality and data correctness

**For more information:** See the main documentation files (`QUICKSTART.md`, `ARCHITECTURE.md`, `API_REFERENCE.md`, `FAQ.md`).
