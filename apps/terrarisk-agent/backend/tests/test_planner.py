from terrarisk.agents.planner import build_planner_steps
from terrarisk.models.domain import AnalysisMode, AnalysisRequest, HazardType


def test_build_planner_steps_includes_required_sources():
    request = AnalysisRequest(
        query="Where should we prioritize hurricane mitigation?",
        mode=AnalysisMode.OFFLINE,
        hazards=[HazardType.HURRICANE],
    )

    result = build_planner_steps(request)

    sources = {step.source for step in result.steps}
    assert "earth_ai_stub" in sources
    assert "nri_loader" in sources
    assert "bigquery_ee" in sources
    assert "report_compose" in sources

    for step in result.steps:
        assert step.description, "Each step should include a human-readable description"
