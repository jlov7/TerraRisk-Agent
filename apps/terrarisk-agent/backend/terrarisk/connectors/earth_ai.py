from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Protocol

from ..config import get_settings
from ..models.domain import PlannerStep


class EarthAIProtocol(Protocol):
    def plan(self, query: str) -> list[PlannerStep]:
        ...

    def run(self, step: PlannerStep) -> dict[str, Any]:
        ...


@dataclass
class EarthAIStubClient(EarthAIProtocol):
    """Offline stub that mimics Google Earth AI multi-step reasoning."""

    def plan(self, query: str) -> list[PlannerStep]:
        seed_steps = [
            PlannerStep(
                id="earth-ai-1",
                description="Decompose query into geospatial objectives using synthetic Gemini reasoning.",
                source="earth_ai_stub",
                inputs=[query],
                parameters={"mode": "analysis"},
            ),
            PlannerStep(
                id="earth-ai-2",
                description="Suggest Earth Engine datasets for hazard overlays.",
                source="earth_ai_stub",
                inputs=["earth-ai-1"],
                parameters={"datasets": ["NOAA_HURRICANE_WIND", "FEMA_FLOOD_ZONES"]},
            ),
        ]
        return seed_steps

    def run(self, step: PlannerStep) -> dict[str, Any]:
        payload = {
            "step_id": step.id,
            "description": step.description,
            "source": step.source,
            "synthetic": True,
            "recommendations": step.parameters.get("datasets", []),
        }
        return payload


class EarthAIRealClient(EarthAIProtocol):
    """Placeholder for the real Earth AI client integration."""

    def __init__(self, api_key: str | None = None, endpoint: str | None = None) -> None:
        self.api_key = api_key
        self.endpoint = endpoint or "https://earthai.googleapis.com/v1beta/queries"

    def plan(self, query: str) -> list[PlannerStep]:
        raise NotImplementedError(
            "Earth AI API access pending. Enable via EARTH_AI_ENABLED=1 once credentials are provisioned."
        )

    def run(self, step: PlannerStep) -> dict[str, Any]:
        raise NotImplementedError(
            "Earth AI execution not yet implemented. Track TODO once API spec is published."
        )


def get_earth_ai_client() -> EarthAIProtocol:
    settings = get_settings()
    if settings.earth_ai_enabled:
        return EarthAIRealClient()
    return EarthAIStubClient()


def serialize_plan(steps: list[PlannerStep]) -> str:
    """Serialize planning steps for logging/provenance."""
    return json.dumps([step.model_dump() for step in steps], indent=2)
