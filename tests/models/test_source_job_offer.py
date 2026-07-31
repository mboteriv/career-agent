from career_agent.models.enums import Source
from career_agent.models.source_job_offer import SourceJobOffer
import pytest


def test_source_job_offer_stores_raw_data():
    raw = {
        "id": "123",
        "title": "Backend Engineer",
    }

    offer = SourceJobOffer(
        source=Source.LEVER,
        raw_data=raw,
    )

    assert offer.raw_data == raw
    assert offer.source == Source.LEVER


def test_source_job_offer_is_immutable():
    offer = SourceJobOffer(
        source=Source.LEVER,
        raw_data={},
    )

    with pytest.raises(Exception):
        offer.source = Source.GREENHOUSE