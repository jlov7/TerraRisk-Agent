from __future__ import annotations

from dataclasses import dataclass
from textwrap import dedent
from typing import Any, Mapping

from google.cloud import bigquery

from ..config import get_settings


def _infer_bigquery_scalar_type(value: Any) -> str:
    if isinstance(value, bool):
        return "BOOL"
    if isinstance(value, int):
        return "INT64"
    if isinstance(value, float):
        return "FLOAT64"
    return "STRING"


REGION_STATS_TEMPLATE = dedent(
    """
    CREATE TEMP TABLE geom_features AS
    SELECT
      geom,
      {boundary_key} AS boundary_id
    FROM `{boundary_table}`;

    CREATE TEMP TABLE raster_source AS
    SELECT
      *
    FROM `{raster_table}`;

    SELECT
      boundary_id,
      stats.{stat_name}
    FROM ST_REGIONSTATS(
      (SELECT geom, boundary_id FROM geom_features),
      (SELECT * FROM raster_source),
      STRUCT(
        {stat_args}
      )
    ) AS stats;
    """
)


@dataclass
class BigQueryEarthEngineClient:
    project: str
    dataset: str

    def _client(self) -> bigquery.Client:
        return bigquery.Client(project=self.project)

    def run_region_stats(
        self,
        *,
        boundary_table: str,
        boundary_key: str,
        raster_table: str,
        stat_name: str = "mean",
        stat_args: str = "sample_size => 1000",
    ) -> bigquery.QueryJob:
        template = REGION_STATS_TEMPLATE.format(
            boundary_table=boundary_table,
            boundary_key=boundary_key,
            raster_table=raster_table,
            stat_name=stat_name,
            stat_args=stat_args,
        )
        job = self._client().query(template)
        return job

    def run_sql(self, sql: str, parameters: Mapping[str, Any] | None = None) -> bigquery.QueryJob:
        job_config = None
        client = self._client()
        if parameters:
            query_parameters = [
                bigquery.ScalarQueryParameter(name, _infer_bigquery_scalar_type(value), value)
                for name, value in parameters.items()
            ]
            job_config = bigquery.QueryJobConfig(query_parameters=query_parameters)
        return client.query(sql, job_config=job_config)


def get_bigquery_client() -> BigQueryEarthEngineClient:
    settings = get_settings()
    if not settings.gcp_project or not settings.bigquery_dataset:
        raise RuntimeError("BigQuery client requires GCP_PROJECT and BQ_DATASET to be set.")
    return BigQueryEarthEngineClient(project=settings.gcp_project, dataset=settings.bigquery_dataset)
