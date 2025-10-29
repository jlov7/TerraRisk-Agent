from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration sourced from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        populate_by_name=True,
    )

    app_name: str = "TerraRisk Agent (Personal R&D)"
    environment: Literal["local", "staging", "production"] = "local"
    earth_ai_enabled: bool = False
    gcp_project: str | None = Field(default=None, alias="GCP_PROJECT")
    bigquery_dataset: str | None = Field(default=None, alias="BQ_DATASET")
    earthengine_project: str | None = Field(default=None, alias="EARTHENGINE_PROJECT")
    action_credential_schema_path: str = (
        "packages/schemas/action_credential_v0.json"
    )
    artifact_dir: str = Field(
        default="examples/artifacts",
        description="Relative or absolute path where report artifacts are stored.",
    )
    otel_exporter_otlp_endpoint: str | None = Field(
        default=None, alias="OTEL_EXPORTER_OTLP_ENDPOINT"
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
