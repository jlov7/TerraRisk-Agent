# TerraRisk Agent Evaluation Harness

Quality assurance system for TerraRisk Agent, ensuring narrative quality, data correctness, and reproducibility.

## Purpose

**Why Evaluations Matter:**
- **Trust**: Verify that TerraRisk Agent produces accurate, reliable outputs
- **Quality**: Ensure narrative summaries match expected quality standards
- **Reproducibility**: Confirm that identical inputs produce identical outputs

## What Gets Evaluated

### 1. Narrative Quality (ROUGE-L F1)

**What It Measures:**
- How well generated summaries match expected "golden" summaries
- Uses longest common subsequence (LCS) matching
- F1 score balances precision and recall

**Target:** ROUGE-L F1 ≥ 0.75

**Why This Matters:**
- Ensures AI-generated narratives are coherent and accurate
- Detects regressions in summary quality
- Validates that planner outputs are meaningful

### 2. Join Integrity

**What It Measures:**
- Ensures geospatial data joins are correct
- Validates county FIPS codes match boundaries
- Verifies hazard data aligns with geography filters

**Target:** 100% integrity

**Why This Matters:**
- Prevents data corruption in geospatial analyses
- Ensures accurate risk assessments
- Critical for insurance and emergency planning use cases

### 3. Reproducibility

**What It Measures:**
- Same inputs produce identical outputs
- Artifact checksums match across runs
- Deterministic execution

**Target:** 100% reproducibility

**Why This Matters:**
- Enables audit trails
- Supports reproducibility requirements
- Critical for compliance and trust

## Running Evaluations

### Basic Usage

```bash
cd apps/terrarisk-agent/backend
uv run python ../evals/run_eval.py
```

**Output:**
```
Evaluating TerraRisk Agent...
ROUGE-L F1: 0.82 ✅ (target: ≥ 0.75)
Join Integrity: 100% ✅
Reproducibility: 100% ✅
All checks passed!
```

### In CI/CD

**GitHub Actions Example:**
```yaml
- name: Run evaluation gate
  run: |
    cd apps/terrarisk-agent/backend
    uv run python ../evals/run_eval.py
  # Fails if any check doesn't meet target
```

**Purpose:** Prevent regressions in narrative quality and data correctness.

## Golden Q&A Format

**File:** `golden_qa.jsonl`

**Format:**
```jsonl
{"query": "Which Gulf Coast counties have highest hurricane risk?", "expected_summary": "Expected narrative here..."}
{"query": "What's the wildfire risk for California?", "expected_summary": "..."}
```

**Adding New Test Cases:**
1. Add query and expected summary to `golden_qa.jsonl`
2. Run evaluation to verify it passes
3. Commit to track quality improvements

## Understanding Results

### ROUGE-L F1 Score

- **1.0**: Perfect match (generated summary exactly matches expected)
- **0.75-0.99**: High quality (minor differences acceptable)
- **< 0.75**: Needs improvement (fails quality gate)

**What Affects Score:**
- Planner decomposition quality
- Connector data accuracy
- Report generation narrative quality

### Join Integrity

- **100%**: All joins are correct
- **< 100%**: Data corruption detected

**What Affects Integrity:**
- County FIPS code matching
- Geographic boundary alignment
- Hazard data filtering

### Reproducibility

- **100%**: Identical inputs produce identical outputs
- **< 100%**: Non-deterministic behavior detected

**What Affects Reproducibility:**
- Random number generation
- Timestamp-dependent logic
- External API calls (in cloud mode)

## Extending Evaluations

### Adding New Metrics

**Example: Adding Precision@K:**
```python
# In run_eval.py
def evaluate_precision_at_k(results, k=5):
    """Measure precision of top K recommendations."""
    # Implementation
    pass
```

### Adding Crisis Scenarios

**Future Enhancement:**
- Crisis response fixtures
- Precision@K for hazard rankings
- Response time metrics

## Best Practices

1. **Run evaluations before committing** to catch regressions early
2. **Add new golden Q&A cases** when extending functionality
3. **Monitor ROUGE-L F1** to track quality trends
4. **Verify join integrity** after data source changes

## Troubleshooting

### "ROUGE-L F1 < 0.75"

**Possible Causes:**
- Planner decomposition changed
- Report generation logic modified
- Golden Q&A expectations outdated

**Solution:**
- Review planner outputs
- Check report generation logic
- Update golden Q&A if expectations changed

### "Join Integrity < 100%"

**Possible Causes:**
- County FIPS code mismatches
- Boundary data inconsistencies
- Hazard data filtering errors

**Solution:**
- Verify FIPS codes in fixtures
- Check boundary provider logic
- Review hazard data filtering

### "Reproducibility < 100%"

**Possible Causes:**
- Random number generation
- Timestamp-dependent logic
- External API calls

**Solution:**
- Seed random number generators
- Use deterministic timestamps in tests
- Mock external API calls

---

**Evaluation harness ensures TerraRisk Agent maintains quality, correctness, and reproducibility—critical for building trustworthy AI systems.**
