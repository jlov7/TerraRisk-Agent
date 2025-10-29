# TerraRisk Evaluations

This folder houses the offline evaluation harness:
- `golden_qa.jsonl` – synthetic multi-step underwriting questions with expected narratives.
- `run_eval.py` – computes a lightweight ROUGE-L F1 approximation against generated action credential summaries. Target ≥ 0.75 before shipping changes.
- Future crisis response fixtures will add precision@K and join-integrity checks.

Run locally with:
```bash
cd apps/terrarisk-agent/backend
uv run python ../evals/run_eval.py
```
