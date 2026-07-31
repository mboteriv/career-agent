from datetime import datetime

from career_agent.models.enums import (
    EmploymentType,
    RemoteType,
    Source,
)
from career_agent.models.job_offer import JobOffer
from career_agent.repositories.job_offer_repository import JobOfferRepository


def test_repository_saves_job_offer():
    repository = JobOfferRepository()

    repository.delete_all()

    job = create_job_offer()

    repository.save(job)

def test_repository_can_be_created():
    repository = JobOfferRepository()

    repository.delete_all()

    assert repository is not None

def create_job_offer(**kwargs) -> JobOffer:
    data = {
        "id": "123",
        "source": Source.GREENHOUSE,
        "url": "https://example.com/job/123",
        "title": "Backend Engineer",
        "company_name": "Example Inc.",
        "description": "Example description",
        "location": "Málaga, Spain",
        "employment_type": EmploymentType.FULL_TIME,
        "remote_type": RemoteType.REMOTE,
        "created_at": datetime.now(),
    }

    data.update(kwargs)
    return JobOffer(**data)

def test_repository_gets_job_offer_by_id():
    repository = JobOfferRepository()

    repository.delete_all()

    job = create_job_offer()

    repository.save(job)

    loaded = repository.get_by_id(
        Source.GREENHOUSE,
        "123",
    )

    assert loaded is not None
    assert loaded.title == job.title
    assert loaded.id == job.id
    assert loaded.source == job.source
    assert loaded.company_name == job.company_name
    assert loaded.location == job.location

def test_repository_delete_all():
    repository = JobOfferRepository()

    repository.delete_all()

    job = create_job_offer()

    repository.save(job)

    repository.delete_all()

    loaded = repository.get_by_id(
        Source.GREENHOUSE,
        "123",
    )

    assert loaded is None

def test_repository_lists_all_job_offers():
    repository = JobOfferRepository()

    repository.delete_all()

    job1 = create_job_offer()

    job2 = create_job_offer(
        id="456",
        title="Frontend Engineer",
    )

    repository.save(job1)
    repository.save(job2)

    jobs = repository.list_all()

    assert len(jobs) == 2
    assert jobs[0].title == "Backend Engineer"
    assert jobs[1].title == "Frontend Engineer"

def test_repository_exists():
    repository = JobOfferRepository()

    repository.delete_all()

    job = create_job_offer()

    repository.save(job)

    assert repository.exists(
        Source.GREENHOUSE,
        "123",
    )

    assert not repository.exists(
        Source.GREENHOUSE,
        "999",
    )

def test_repository_saves_multiple_job_offers():
    repository = JobOfferRepository()

    repository.delete_all()

    jobs = [
        create_job_offer(),
        create_job_offer(
            id="456",
            title="Frontend Engineer",
        ),
        create_job_offer(
            id="789",
            title="Data Engineer",
        ),
    ]

    repository.save_all(jobs)

    loaded = repository.list_all()

    assert len(loaded) == 3