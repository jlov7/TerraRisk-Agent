from __future__ import annotations

import uuid
from pathlib import Path
from typing import Any

from ..agents.planner import build_planner_steps
from ..connectors.boundaries import BoundaryProvider
from ..connectors.nri import NRILoader
from ..models.domain import (
    ActionCredential,
    AnalysisRequest,
    AnalysisResponse,
    Artifact,
    HazardType,
    PlannerStep,
)
from ..reports.compose import build_report_bundle
from ..utils.provenance import create_action_credential


def _load_nri_samples() -> list[dict[str, Any]]:
    data_path = Path(__file__).resolve().parent.parent / "examples" / "offline_nri.csv"
    loader = NRILoader(source_path=data_path)
    frame = loader.load()
    if frame.empty:
        return []
    return frame.to_dict(orient="records")


def _steps_to_credentials(steps: list[PlannerStep]) -> list[ActionCredential]:
    credentials: list[ActionCredential] = []
    for step in steps:
        artifacts: list[Artifact] = []
        credential = create_action_credential(
            action_type=f"planner.step.{step.source}",
            inputs=step.inputs,
            outputs=[step.id],
            source=step.source,
            artifacts=artifacts,
            claims=[{"name": "description", "value": step.description}],
            mode=None,
        )
        credentials.append(credential)
    return credentials


def _selected_hazards(request: AnalysisRequest) -> list[str]:
    if request.hazards:
        return [haz.value for haz in request.hazards]

    query = request.query.lower()
    inferred = [haz.value for haz in HazardType if haz.value in query]
    return inferred or [HazardType.HURRICANE.value]


def _summary_highlight(records: list[dict[str, Any]], hazards: list[str]) -> str | None:
    if not records:
        return None

    top_record = records[0]
    primary_hazard = hazards[0] if hazards else str(top_record["hazard_type"])
    if primary_hazard == HazardType.HURRICANE.value and len(records) > 1:
        return (
            f"{top_record['county']} and {records[1]['county']} show elevated "
            f"{primary_hazard} EAL"
        )
    if primary_hazard == HazardType.FLOOD.value:
        return f"{top_record['county']} flood hot spots with high population"
    if primary_hazard == HazardType.WILDFIRE.value:
        return f"{top_record['county']} wildfire exposure requires mitigation priority"
    return f"{top_record['county']} shows elevated {primary_hazard} EAL"


def run_analysis(request: AnalysisRequest) -> AnalysisResponse:
    run_id = str(uuid.uuid4())

    planner_result = build_planner_steps(request)
    planner_credentials = _steps_to_credentials(planner_result.steps)

    nri_records = _load_nri_samples()

    selected_hazards = _selected_hazards(request)
    ranked = [
        record
        for record in nri_records
        if record["hazard_type"] in selected_hazards
    ]
    ranked.sort(key=lambda item: item["eal"], reverse=True)

    boundary_provider = BoundaryProvider()
    features = [boundary_provider.county_feature(item["county_fips"]) for item in ranked]

    detail_highlights = [
        f"{item['county']} ({item['county_fips']}): EAL {item['eal']} with resilience index {item['resilience_index']}"
        for item in ranked
    ]
    summary_highlight = _summary_highlight(ranked, selected_hazards)
    highlights = [summary_highlight, *detail_highlights] if summary_highlight else detail_highlights
    sources = [
        "Synthetic Earth AI reasoning trace",
        "FEMA National Risk Index (offline fixture)",
        "BigQuery Earth Engine (template placeholders)",
    ]
    portfolio_rows = [
        {
            "portfolio_id": request.portfolio_reference or "demo-portfolio",
            "county_fips": item["county_fips"],
            "hazard": item["hazard_type"],
            "eal": item["eal"],
        }
        for item in ranked
    ]

    artifacts, report_credentials = build_report_bundle(
        request,
        run_id=run_id,
        highlights=highlights,
        summary=summary_highlight,
        sources=sources,
        features=features,
        portfolio_rows=portfolio_rows,
    )

    return AnalysisResponse(
        run_id=run_id,
        steps=planner_result.steps,
        artifacts=artifacts,
        action_credentials=[*planner_credentials, *report_credentials],
        highlights=highlights,
        sources=sources,
    )
