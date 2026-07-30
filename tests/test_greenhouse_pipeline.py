from career_agent.collectors.greenhouse_collector import GreenhouseCollector
from career_agent.normalizers.job_offer_normalizer import JobOfferNormalizer
from career_agent.parsers.greenhouse_parser import GreenhouseParser

from tests.helpers import load_fixture


def test_greenhouse_pipeline():

    payload = load_fixture(
        "greenhouse",
        "jobs.json",
    )

    collector = GreenhouseCollector()
    parser = GreenhouseParser()
    normalizer = JobOfferNormalizer()

    source_offers = collector.collect(payload)

    jobs = [
        normalizer.normalize(
            parser.parse(source_offer)
        )
        for source_offer in source_offers
    ]

    assert len(jobs) == 2

    assert jobs[0].title == "Backend Engineer"
    assert jobs[1].title == "Frontend Engineer"