from __future__ import annotations

from pathlib import Path
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Path as ApiPath
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

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


def _artifact_dir(settings: Settings) -> Path:
    configured = Path(settings.artifact_dir)
    if not configured.is_absolute():
        configured = Path(__file__).resolve().parent / configured
    configured.mkdir(parents=True, exist_ok=True)
    return configured


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


@app.get("/artifacts/{filename}")
def get_artifact(
    filename: Annotated[str, ApiPath(..., description="Artifact filename")],
    settings: Annotated[Settings, Depends(get_app_settings)],
) -> FileResponse:
    safe_name = Path(filename).name
    artifact_path = _artifact_dir(settings) / safe_name
    if not artifact_path.exists():
        raise HTTPException(status_code=404, detail="Artifact not found")
    return FileResponse(artifact_path)


@app.get("/scenarios/{hazard}", response_model=ScenarioResponse)
def scenario(hazard: Annotated[HazardType, ApiPath(..., description="Hazard scenario key")]) -> ScenarioResponse:
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
