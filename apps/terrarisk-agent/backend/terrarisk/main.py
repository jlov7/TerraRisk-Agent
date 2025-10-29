from __future__ import annotations

from typing import Annotated

from fastapi import Depends, FastAPI, Path
from fastapi.middleware.cors import CORSMiddleware

from .config import Settings, get_settings
from .models.domain import (
    AnalysisMode,
    AnalysisRequest,
    AnalysisResponse,
    Artifact,
    HazardType,
    PortfolioStressResponse,
    ScenarioResponse,
)
from .services.analysis import run_analysis

app = FastAPI(
    title="TerraRisk Agent API",
    description="Personal passion R&D copilot for geospatial underwriting and response.",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_app_settings() -> Settings:
    return get_settings()


@app.get("/healthz")
def healthcheck(settings: Annotated[Settings, Depends(get_app_settings)]) -> dict[str, str]:
    return {"status": "ok", "mode": "cloud" if settings.earth_ai_enabled else "offline"}


@app.post("/analyze", response_model=AnalysisResponse)
def analyze(request: AnalysisRequest) -> AnalysisResponse:
    return run_analysis(request)


@app.post("/report", response_model=AnalysisResponse)
def report(request: AnalysisRequest) -> AnalysisResponse:
    response = run_analysis(request)
    return response


@app.get("/scenarios/{hazard}", response_model=ScenarioResponse)
def scenario(hazard: Annotated[HazardType, Path(..., description="Hazard scenario key")]) -> ScenarioResponse:
    summary = f"Synthetic {hazard.value} scenario for offline mode."
    metrics = {"risk_score": 0.7, "exposed_population": 125000}
    recommended_actions = [
        "Pre-position mitigation assets",
        "Coordinate evacuation routes with local agencies",
        "Verify shelter capacity against population-at-risk",
    ]
    artifacts: list[Artifact] = []
    return ScenarioResponse(
        scenario=hazard,
        summary=summary,
        metrics=metrics,
        recommended_actions=recommended_actions,
        artifacts=artifacts,
    )


@app.post("/portfolio/stress", response_model=PortfolioStressResponse)
def portfolio_stress(portfolio_id: str, mode: AnalysisMode = AnalysisMode.OFFLINE) -> PortfolioStressResponse:
    summary = f"Stress test for portfolio {portfolio_id} in mode {mode.value}."
    metrics = {"pml": 0.82, "tail_value_at_risk": 0.21}
    artifacts: list[Artifact] = []
    return PortfolioStressResponse(
        portfolio_id=portfolio_id,
        summary=summary,
        metrics=metrics,
        artifacts=artifacts,
    )
