from career_agent.dto.source_job_offer import SourceJobOffer
from career_agent.models.enums import Source
from career_agent.parsers.greenhouse_parser import GreenhouseParser

from tests.helpers import load_fixture

from datetime import UTC, datetime


def test_parser_creates_parsed_job_offer():

    payload = load_fixture(
        "greenhouse",
        "job.json",
    )

    source = SourceJobOffer(
        source=Source.GREENHOUSE,
        payload=payload,
        collected_at=datetime.now(UTC),
    )

    parsed = GreenhouseParser().parse(source)

    assert parsed.title == payload["title"]
    assert parsed.company_name == payload["company_name"]
    assert parsed.description == payload["content"]
    assert parsed.location == payload["location"]["name"]
    assert parsed.source_url == payload["absolute_url"]

    assert parsed.source == Source.GREENHOUSE
    assert parsed.collected_at == source.collected_at