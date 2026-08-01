from unittest import result

from career_agent.collectors.greenhouse_collector import GreenhouseCollector
from career_agent.parsers.greenhouse_parser import GreenhouseParser
from career_agent.services.job_import_service import JobImportService
from career_agent.providers.greenhouse_provider import greenhouse_provider
from career_agent.repositories.job_offer_repository import (
    JobOfferRepository,
)
from career_agent.testing.factories import create_job_offer
from career_agent.models.enums import Source

def test_import_jobs():
    repository = JobOfferRepository()
    repository.delete_all()

    service = JobImportService(
        provider=greenhouse_provider(),
    )

    result = service.import_jobs("canonical")

    assert len(result.new_jobs) > 0
    assert result.updated_jobs == []
    assert result.removed_jobs == []
    assert result.unchanged_jobs == []

def test_import_jobs_twice_detects_unchanged_jobs():

    repository = JobOfferRepository()
    repository.delete_all()

    service = JobImportService(
        provider=greenhouse_provider(),
        repository=repository,
    )

    first = service.import_jobs("canonical")

    assert len(first.new_jobs) > 0

    second = service.import_jobs("canonical")

    assert second.new_jobs == []
    assert second.updated_jobs == []
    assert len(second.unchanged_jobs) > 0

def test_import_detects_updated_job():

    repository = JobOfferRepository()
    repository.delete_all()

    service = JobImportService(
        provider=greenhouse_provider(),
        repository=repository,
    )

    job = create_job_offer()

    repository.save(job)

    updated = create_job_offer(
        title="Senior Backend Engineer",
    )

    new_jobs = []
    updated_jobs = []
    unchanged_jobs = []

    service._classify_job(
        updated,
        new_jobs,
        updated_jobs,
        unchanged_jobs,
    )

    loaded = repository.get_by_id(
        Source.GREENHOUSE,
        "123",
    )

    assert new_jobs == []
    assert len(updated_jobs) == 1
    assert unchanged_jobs == []
    assert loaded.title == "Senior Backend Engineer"