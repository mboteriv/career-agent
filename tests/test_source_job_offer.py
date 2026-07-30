from datetime import datetime

import pytest
from pydantic import ValidationError

from career_agent.dto.source_job_offer import SourceJobOffer
from career_agent.models.enums import Source


def create_source_job_offer(**kwargs) -> SourceJobOffer:
    data = {
        "source": Source.GREENHOUSE,
        "payload": {
            "id": 123,
            "title": "Backend Engineer",
            "company": "Example Inc.",
        },
        "collected_at": datetime.now(),
    }

    data.update(kwargs)
    return SourceJobOffer(**data)


def test_create_source_job_offer():
    offer = create_source_job_offer()

    assert offer.source == Source.GREENHOUSE
    assert offer.payload["title"] == "Backend Engineer"


def test_source_job_offer_is_immutable():
    offer = create_source_job_offer()

    with pytest.raises(ValidationError):
        offer.source = Source.LEVER


def test_source_job_offer_preserves_payload():
    payload = {
        "id": 999,
        "title": "Senior Python Engineer",
        "location": "Madrid",
    }

    offer = create_source_job_offer(payload=payload)

    assert offer.payload == payload


def test_invalid_source_raises_validation_error():
    with pytest.raises(ValidationError):
        create_source_job_offer(
            source="linkedin"
        )