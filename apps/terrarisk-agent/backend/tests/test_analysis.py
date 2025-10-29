from terrarisk.models.domain import AnalysisMode, AnalysisRequest
from terrarisk.services.analysis import run_analysis


def test_run_analysis_offline_generates_artifacts(tmp_path, monkeypatch):
    request = AnalysisRequest(
        query="Identify top hurricane risk counties near the Gulf Coast.",
        mode=AnalysisMode.OFFLINE,
    )

    response = run_analysis(request)

    assert response.artifacts, "Expected offline mode to produce artifacts"
    assert response.action_credentials, "Expected provenance credentials per step"
    assert any("report.compose" in cred.action["type"] for cred in response.action_credentials)
