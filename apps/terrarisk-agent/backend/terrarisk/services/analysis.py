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


def run_analysis(request: AnalysisRequest) -> AnalysisResponse:
    run_id = str(uuid.uuid4())

    planner_result = build_planner_steps(request)
    planner_credentials = _steps_to_credentials(planner_result.steps)

    nri_records = _load_nri_samples()

    selected_hazards = [haz.value for haz in request.hazards or [HazardType.HURRICANE]]
    ranked = [
        record
        for record in nri_records
        if record["hazard_type"] in selected_hazards
    ]
    ranked.sort(key=lambda item: item["eal"], reverse=True)

    boundary_provider = BoundaryProvider()
    features = [boundary_provider.county_feature(item["county_fips"]) for item in ranked]

    highlights = [
        f"{item['county']} ({item['county_fips']}): EAL {item['eal']} with resilience index {item['resilience_index']}"
        for item in ranked
    ]
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
        sources=sources,
        features=features,
        portfolio_rows=portfolio_rows,
    )

    return AnalysisResponse(
        run_id=run_id,
        steps=planner_result.steps,
        artifacts=artifacts,
        action_credentials=[*planner_credentials, *report_credentials],
    )
