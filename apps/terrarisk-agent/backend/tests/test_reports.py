from pathlib import Path

from terrarisk import config
from terrarisk.models.domain import AnalysisMode, AnalysisRequest
from terrarisk.reports.compose import build_report_bundle


def test_build_report_bundle_respects_artifact_dir(tmp_path, monkeypatch):
    monkeypatch.setenv("ARTIFACT_DIR", str(tmp_path))
    config.get_settings.cache_clear()

    request = AnalysisRequest(query="Demo query", mode=AnalysisMode.OFFLINE)

    artifacts, credentials = build_report_bundle(
        request,
        run_id="unit-test",
        highlights=["County A high risk"],
        sources=["Synthetic data"],
        features=[{"type": "Feature", "geometry": None, "properties": {}}],
        portfolio_rows=[{"portfolio_id": "demo", "metric": "eal", "value": 0.5}],
    )

    assert artifacts, "Expected artifacts to be created"
    for artifact in artifacts:
        path = Path(artifact.uri)
        assert path.exists()
        assert str(path).startswith(str(tmp_path))

    assert credentials, "Expected an action credential for the report step"
    config.get_settings.cache_clear()
