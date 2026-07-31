import pytest
from pydantic import ValidationError

from career_agent.models.enums import Source
from career_agent.models.source_job_offer import SourceJobOffer


def create_source_job_offer(**kwargs) -> SourceJobOffer:
    data = {
    "source": Source.GREENHOUSE,
    "raw_data": {
        "id": 123,
        "title": "Backend Engineer",
        "company": "Example Inc.",
    },
    "metadata": {},
}

    data.update(kwargs)
    return SourceJobOffer(**data)


def test_create_source_job_offer():
    offer = create_source_job_offer()

    assert offer.source == Source.GREENHOUSE
    assert offer.raw_data["title"] == "Backend Engineer"


def test_source_job_offer_is_immutable():
    offer = create_source_job_offer()

    with pytest.raises(Exception):
        offer.source = Source.LEVER


def test_source_job_offer_preserves_payload():
    payload = {
        "id": 999,
        "title": "Senior Python Engineer",
        "location": "Madrid",
    }

    offer = create_source_job_offer(raw_data=payload)

    assert offer.raw_data == payload


def test_invalid_source_raises_validation_error():
    with pytest.raises(Exception):
        create_source_job_offer(
            source="linkedin"
        )

def test_source_job_offer_stores_metadata():
    offer = SourceJobOffer(
        source=Source.LEVER,
        raw_data={},
        metadata={
            "company_name": "Canonical",
            "board": "canonical",
        },
    )

    assert offer.metadata["company_name"] == "Canonical"
    assert offer.metadata["board"] == "canonical"