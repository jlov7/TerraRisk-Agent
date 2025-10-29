from __future__ import annotations

import uuid
from typing import Iterable

from ..connectors.earth_ai import get_earth_ai_client
from ..models.domain import AnalysisRequest, PlannerResult, PlannerStep


def build_planner_steps(request: AnalysisRequest) -> PlannerResult:
    earth_ai = get_earth_ai_client()
    earth_ai_steps = earth_ai.plan(request.query)

    supplemental_steps: list[PlannerStep] = [
        PlannerStep(
            id=str(uuid.uuid4()),
            description="Load FEMA NRI metrics for requested geographies.",
            source="nri_loader",
            inputs=request.geography_filter or [],
            parameters={"hazards": [haz.value for haz in request.hazards or []]},
        ),
        PlannerStep(
            id=str(uuid.uuid4()),
            description="Join hazard metrics with BigQuery Earth Engine aggregations.",
            source="bigquery_ee",
            inputs=[step.id for step in earth_ai_steps],
            parameters={"mode": request.mode.value},
        ),
        PlannerStep(
            id=str(uuid.uuid4()),
            description="Compose mitigation narrative and ranking.",
            source="report_compose",
            inputs=[],
            parameters={"portfolio_reference": request.portfolio_reference},
        ),
    ]

    steps: Iterable[PlannerStep] = (*earth_ai_steps, *supplemental_steps)
    return PlannerResult(steps=list(steps))
