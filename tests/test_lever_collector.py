import json
from pathlib import Path

from career_agent.collectors.lever_collector import LeverCollector
from career_agent.models.source_job_offer import SourceJobOffer


def test_collect_creates_source_job_offers():
    fixture = Path("tests/fixtures/lever/jobs.json")

    with fixture.open(encoding="utf-8") as f:
        payload = json.load(f)

    collector = LeverCollector()

    offers = collector.collect(payload)

    assert len(offers) == 2
    assert isinstance(offers[0], SourceJobOffer)
    assert offers[0].raw_data == payload[0]
    assert offers[1].raw_data == payload[1]