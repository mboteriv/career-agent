from datetime import datetime

import pytest
from pydantic import ValidationError

from career_agent.dto.parsed_job_offer import ParsedJobOffer
from career_agent.models.enums import Source


def create_parsed_job_offer(**kwargs) -> ParsedJobOffer:
    data = {
        "source": Source.GREENHOUSE,
        "collected_at": datetime.now(),
        "title": "Backend Engineer",
        "company_name": "Example Inc.",
        "description": "Example description",
        "location": "Málaga, Spain",
        "employment_type": "Full Time",
        "remote_type": "Hybrid",
        "source_url": "https://example.com/job/123",
    }

    data.update(kwargs)
    return ParsedJobOffer(**data)

def test_create_parsed_job_offer():
    offer = create_parsed_job_offer()

    assert offer.title == "Backend Engineer"
    assert offer.company_name == "Example Inc."

def test_parsed_job_offer_is_immutable():
    offer = create_parsed_job_offer()

    with pytest.raises(ValidationError):
        offer.title = "Frontend Engineer"

def test_parsed_job_offer_preserves_original_values():
    offer = create_parsed_job_offer(
        employment_type="Permanent",
        remote_type="Remote"
    )

    assert offer.employment_type == "Permanent"
    assert offer.remote_type == "Remote"

def test_missing_required_field_raises_validation_error():
    data = create_parsed_job_offer().model_dump()
    del data["title"]

    with pytest.raises(ValidationError):
        ParsedJobOffer(**data)