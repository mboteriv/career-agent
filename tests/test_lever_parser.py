from career_agent.models.enums import Source
from career_agent.models.source_job_offer import SourceJobOffer
from career_agent.parsers.lever_parser import LeverParser

from tests.helpers import load_fixture


def test_parser_extracts_title():
    payload = load_fixture(
        "lever",
        "job.json",
    )

    source_offer = SourceJobOffer(
        source=Source.LEVER,
        raw_data=payload,
        metadata={
            "company_name": "Canonical",
            "board": "canonical",
        },
    )

    parsed = LeverParser().parse(source_offer)

    assert parsed.title == payload["text"]
    assert parsed.id == payload["id"]
    assert parsed.url == payload["hostedUrl"]
    assert parsed.description == payload["description"]
    assert parsed.location == payload["categories"]["location"]
    assert parsed.employment_type == payload["categories"]["commitment"]
    assert parsed.remote_type is None
    assert parsed.company_name == "Canonical"