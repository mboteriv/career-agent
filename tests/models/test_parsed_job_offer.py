from career_agent.models.enums import Source
from career_agent.models.parsed_job_offer import ParsedJobOffer
import pytest


def test_parsed_job_offer_stores_parsed_data():
    offer = ParsedJobOffer(
        id="123",
        source=Source.LEVER,
        url="https://example.com/jobs/123",
        title="Backend Engineer",
        company_name="Example Inc.",
        description="Example description",
        location="Madrid",
        employment_type="Full-time",
        remote_type="remote",
    )

    assert offer.title == "Backend Engineer"
    assert offer.company_name == "Example Inc."
    assert offer.employment_type == "Full-time"
    assert offer.remote_type == "remote"

def test_parsed_job_offer_is_immutable():
    offer = ParsedJobOffer(
        id="123",
        source=Source.LEVER,
        url="https://example.com/jobs/123",
        title="Backend Engineer",
        company_name="Example Inc.",
        description="Example description",
        location="Madrid",
    )

    with pytest.raises(Exception):
        offer.title = "Frontend Engineer"