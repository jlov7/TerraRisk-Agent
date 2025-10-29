from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Sequence

from pydantic import BaseModel, Field


class AnalysisMode(str, Enum):
    CLOUD = "cloud"
    BYO_BIGQUERY = "byo_bigquery"
    OFFLINE = "offline"


class HazardType(str, Enum):
    HURRICANE = "hurricane"
    WILDFIRE = "wildfire"
    FLOOD = "flood"


class PlannerStep(BaseModel):
    id: str
    description: str
    source: str
    inputs: list[str] = Field(default_factory=list)
    parameters: dict[str, Any] = Field(default_factory=dict)


class PlannerResult(BaseModel):
    steps: list[PlannerStep]


class Artifact(BaseModel):
    uri: str
    type: str
    hash: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class ActionCredential(BaseModel):
    version: str = "0.1.0"
    id: str
    timestamp: datetime
    actor: dict[str, Any]
    action: dict[str, Any]
    artifacts: Sequence[Artifact]
    claims: Sequence[dict[str, Any]]
    signatures: Sequence[dict[str, Any]] = Field(default_factory=list)
    trace: dict[str, Any] | None = None


class AnalysisRequest(BaseModel):
    query: str
    geography_filter: list[str] | None = None
    hazards: list[HazardType] | None = None
    mode: AnalysisMode = AnalysisMode.OFFLINE
    portfolio_reference: str | None = None
    allow_pii: bool = False


class AnalysisResponse(BaseModel):
    run_id: str
    steps: list[PlannerStep]
    artifacts: list[Artifact]
    action_credentials: list[ActionCredential]


class ScenarioResponse(BaseModel):
    scenario: HazardType
    summary: str
    metrics: dict[str, Any]
    recommended_actions: list[str]
    artifacts: list[Artifact]


class PortfolioStressResponse(BaseModel):
    portfolio_id: str
    summary: str
    metrics: dict[str, Any]
    artifacts: list[Artifact]
