from terrarisk.main import app
from terrarisk.models.domain import HazardType

from fastapi.testclient import TestClient


def test_scenario_endpoint_covers_all_hazards():
    client = TestClient(app)
    for hazard in HazardType:
        response = client.get(f"/scenarios/{hazard.value}")
        assert response.status_code == 200
        payload = response.json()
        assert payload["scenario"] == hazard.value
        assert payload["recommended_actions"], "Expected recommended actions for each hazard"
