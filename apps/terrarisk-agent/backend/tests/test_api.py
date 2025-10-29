from pathlib import Path

from fastapi.testclient import TestClient

from terrarisk import config
from terrarisk.main import app


def test_analyze_endpoint_generates_artifacts(tmp_path, monkeypatch):
    monkeypatch.setenv("ARTIFACT_DIR", str(tmp_path))
    config.get_settings.cache_clear()

    client = TestClient(app)
    payload = {
        "query": "Which counties near the Gulf Coast face elevated hurricane risk?",
        "mode": "offline",
        "hazards": ["hurricane"],
    }

    response = client.post("/analyze", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["artifacts"], "Expected artifacts in response payload"

    for artifact in body["artifacts"]:
        path = Path(artifact["uri"])
        assert path.exists()
        assert str(path).startswith(str(tmp_path))

    config.get_settings.cache_clear()
