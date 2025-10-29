from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable, Tuple

from jinja2 import Template

from ..config import get_settings
from ..models.domain import AnalysisRequest, Artifact
from ..utils.provenance import create_action_credential


REPORT_TEMPLATE = Template(
    """
    <html>
    <head>
      <style>
        body { font-family: sans-serif; margin: 2rem; }
        h1 { color: #1b4d89; }
      </style>
    </head>
    <body>
      <h1>TerraRisk Mitigation Brief</h1>
      <p><strong>Query:</strong> {{ query }}</p>
      <p><strong>Mode:</strong> {{ mode }}</p>
      <h2>Highlights</h2>
      <ul>
        {% for item in highlights %}
          <li>{{ item }}</li>
        {% endfor %}
      </ul>
      <h2>Data Sources</h2>
      <ul>
        {% for source in sources %}
          <li>{{ source }}</li>
        {% endfor %}
      </ul>
      <footer>
        <p>Personal passion R&D project — provenance stitched via Action Credentials.</p>
      </footer>
    </body>
    </html>
    """
)


def _hash_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _artifact_dir() -> Path:
    settings = get_settings()
    configured = Path(settings.artifact_dir)
    if not configured.is_absolute():
        base = Path(__file__).resolve().parent.parent
        configured = base / configured
    configured.mkdir(parents=True, exist_ok=True)
    return configured


def _write_pdf(run_id: str, html: str) -> Path:
    pdf_path = _artifact_dir() / f"{run_id}_report.pdf"
    # Using simple write for placeholder, real implementation should render with WeasyPrint.
    pdf_path.write_text("PDF placeholder for offline mode.\n\n" + html)
    return pdf_path


def _write_geojson(run_id: str, features: Iterable[dict[str, Any]]) -> Path:
    geojson_path = _artifact_dir() / f"{run_id}_layers.geojson"
    content = {"type": "FeatureCollection", "features": list(features)}
    geojson_path.write_text(json.dumps(content))
    return geojson_path


def _write_csv(run_id: str, rows: Iterable[dict[str, Any]]) -> Path:
    csv_path = _artifact_dir() / f"{run_id}_portfolio_diff.csv"
    rows = list(rows)
    if not rows:
        csv_path.write_text("portfolio_id,metric,value\n")
        return csv_path
    with csv_path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return csv_path


def build_report_bundle(
    request: AnalysisRequest,
    *,
    run_id: str,
    highlights: list[str],
    sources: list[str],
    features: Iterable[dict[str, Any]],
    portfolio_rows: Iterable[dict[str, Any]],
) -> Tuple[list[Artifact], list]:
    html = REPORT_TEMPLATE.render(
        query=request.query,
        mode=request.mode.value,
        highlights=highlights,
        sources=sources,
    )
    pdf_path = _write_pdf(run_id, html)
    geojson_path = _write_geojson(run_id, features)
    csv_path = _write_csv(run_id, portfolio_rows)

    artifacts = [
        Artifact(uri=str(pdf_path), type="application/pdf", hash=_hash_bytes(pdf_path.read_bytes())),
        Artifact(uri=str(geojson_path), type="application/geo+json", hash=_hash_bytes(geojson_path.read_bytes())),
        Artifact(uri=str(csv_path), type="text/csv", hash=_hash_bytes(csv_path.read_bytes())),
    ]

    credential = create_action_credential(
        action_type="report.compose",
        inputs=[request.query],
        outputs=[artifact.uri for artifact in artifacts],
        source="reports.compose",
        artifacts=artifacts,
        claims=[{"name": "mode", "value": request.mode.value}],
        mode=request.mode.value,
    )

    return artifacts, [credential]
