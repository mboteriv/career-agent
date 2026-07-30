from career_agent.collectors.greenhouse_collector import GreenhouseCollector
from career_agent.models.enums import Source

from tests.helpers import load_fixture


def test_collector_creates_source_job_offers():

    payload = load_fixture(
        "greenhouse",
        "jobs.json",
    )

    collector = GreenhouseCollector()

    offers = collector.collect(payload)

    assert len(offers) == 2

    assert offers[0].source == Source.GREENHOUSE
    assert offers[1].source == Source.GREENHOUSE
    assert offers[0].payload["title"] == "Backend Engineer"
    assert offers[1].payload["title"] == "Frontend Engineer"

    assert offers[0].payload["id"] == 12345
    assert offers[1].payload["id"] == 12346
    assert offers[0].collected_at == offers[1].collected_at