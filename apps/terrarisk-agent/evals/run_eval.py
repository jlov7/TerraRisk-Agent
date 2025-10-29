from __future__ import annotations

import argparse
import json
from pathlib import Path
from difflib import SequenceMatcher

from terrarisk.models.domain import AnalysisMode, AnalysisRequest
from terrarisk.services.analysis import run_analysis


def rouge_l_f1(reference: str, prediction: str) -> float:
    matcher = SequenceMatcher(None, reference, prediction)
    lcs = sum(triple.size for triple in matcher.get_matching_blocks())
    if lcs == 0:
        return 0.0
    precision = lcs / len(prediction)
    recall = lcs / len(reference)
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


def evaluate(dataset_path: Path) -> float:
    scores: list[float] = []
    with dataset_path.open() as handle:
        for line in handle:
            record = json.loads(line)
            request = AnalysisRequest(query=record["query"], mode=AnalysisMode.OFFLINE)
            response = run_analysis(request)
            snippets = []
            for credential in response.action_credentials:
                for claim in credential.claims:
                    if claim.get("name") == "description":
                        snippets.append(str(claim.get("value")))
            narrative = " ".join(snippets)
            score = rouge_l_f1(record["expected_summary"], narrative)
            scores.append(score)
    return sum(scores) / len(scores)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run TerraRisk offline evaluation harness")
    parser.add_argument("--dataset", type=Path, default=Path(__file__).parent / "golden_qa.jsonl")
    args = parser.parse_args()

    score = evaluate(args.dataset)
    threshold = 0.75
    print(f"ROUGE-L F1: {score:.3f} (target ≥ {threshold})")
    if score < threshold:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
