from terrarisk.connectors.earth_ai import EarthAIStubClient


def test_earth_ai_stub_plan_and_run_cycle():
    client = EarthAIStubClient()
    query = "Assess hurricane and flood risk"
    steps = client.plan(query)

    assert len(steps) >= 2
    assert steps[0].inputs == [query]

    output = client.run(steps[0])
    assert output["step_id"] == steps[0].id
    assert output["synthetic"] is True
