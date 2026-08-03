from datetime import datetime

from career_agent.models.enums import (
    EmploymentType,
    RemoteType,
    Source,
)
from career_agent.models.job_offer import JobOffer
from career_agent.models.job_search_criteria import JobSearchCriteria
from career_agent.repositories.job_offer_repository import JobOfferRepository
from tests.factories import create_job_offer
from career_agent.models.job_sort_field import JobSortField
from career_agent.models.salary_expectation import (
    SalaryExpectation,
)


def test_repository_saves_job_offer():
    repository = JobOfferRepository()

    repository.delete_all()

    job = create_job_offer()

    repository.save(job)

def test_repository_can_be_created():
    repository = JobOfferRepository()

    repository.delete_all()

    assert repository is not None



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

def test_repository_updates_job_offer():

    repository = JobOfferRepository()

    repository.delete_all()

    job = create_job_offer()

    repository.save(job)

    updated = create_job_offer(
        title="Senior Backend Engineer",
    )

    repository.update(updated)

    loaded = repository.get_by_id(
        Source.GREENHOUSE,
        "123",
    )

    assert loaded.title == "Senior Backend Engineer"

def test_repository_lists_jobs_by_source():

    repository = JobOfferRepository()

    repository.delete_all()

    repository.save(
        create_job_offer(
            id="1",
            source=Source.GREENHOUSE,
        )
    )

    repository.save(
        create_job_offer(
            id="2",
            source=Source.GREENHOUSE,
        )
    )

    repository.save(
        create_job_offer(
            id="1",
            source=Source.LEVER,
        )
    )

    jobs = repository.list_by_source(
        Source.GREENHOUSE,
    )

    assert len(jobs) == 2

def test_repository_deletes_job_offer():

    repository = JobOfferRepository()

    repository.delete_all()

    repository.save(
        create_job_offer()
    )

    repository.delete(
        Source.GREENHOUSE,
        "123",
    )

    loaded = repository.get_by_id(
        Source.GREENHOUSE,
        "123",
    )

    assert loaded is None


def test_repository_searches_by_company_name():

    repository = JobOfferRepository()

    repository.delete_all()

    repository.save(
        create_job_offer(
            id="1",
            company_name="Canonical",
        )
    )

    repository.save(
        create_job_offer(
            id="2",
            company_name="GitLab",
        )
    )

    criteria = JobSearchCriteria(
        company_name="Canonical",
    )

    jobs = repository.search(criteria)

    assert len(jobs) == 1
    assert jobs[0].company_name == "Canonical"

def test_repository_searches_by_location():

    repository = JobOfferRepository()

    repository.delete_all()

    repository.save(
        create_job_offer(
            id="1",
            location="Spain",
        )
    )

    repository.save(
        create_job_offer(
            id="2",
            location="Germany",
        )
    )

    criteria = JobSearchCriteria(
        location="Spain",
    )

    jobs = repository.search(criteria)

    assert len(jobs) == 1
    assert jobs[0].location == "Spain"

def test_repository_searches_by_remote_type():

    repository = JobOfferRepository()

    repository.delete_all()

    repository.save(
        create_job_offer(
            id="1",
            remote_type=RemoteType.REMOTE,
        )
    )

    repository.save(
        create_job_offer(
            id="2",
            remote_type=RemoteType.HYBRID,
        )
    )

    criteria = JobSearchCriteria(
        remote_type=RemoteType.REMOTE,
    )

    jobs = repository.search(criteria)

    assert len(jobs) == 1
    assert jobs[0].remote_type is RemoteType.REMOTE

def test_repository_searches_by_employment_type():

    repository = JobOfferRepository()

    repository.delete_all()

    repository.save(
        create_job_offer(
            id="1",
            employment_type=EmploymentType.FULL_TIME,
        )
    )

    repository.save(
        create_job_offer(
            id="2",
            employment_type=EmploymentType.CONTRACT,
        )
    )

    criteria = JobSearchCriteria(
        employment_type=EmploymentType.FULL_TIME,
    )

    jobs = repository.search(criteria)

    assert len(jobs) == 1
    assert jobs[0].employment_type is EmploymentType.FULL_TIME

def test_repository_searches_by_keyword():

    repository = JobOfferRepository()

    repository.delete_all()

    repository.save(
        create_job_offer(
            id="1",
            title="Senior Python Developer",
            description="Build backend APIs",
        )
    )

    repository.save(
        create_job_offer(
            id="2",
            title="Frontend Engineer",
            description="React and TypeScript",
        )
    )

    criteria = JobSearchCriteria(
        keywords=["python"],
    )

    jobs = repository.search(criteria)

    assert len(jobs) == 1
    assert jobs[0].id == "1"

def test_repository_searches_by_multiple_keywords():

    repository = JobOfferRepository()

    repository.delete_all()

    repository.save(
        create_job_offer(
            id="1",
            title="Senior Python Developer",
        )
    )

    repository.save(
        create_job_offer(
            id="2",
            title="Django Backend Engineer",
        )
    )

    repository.save(
        create_job_offer(
            id="3",
            title="Frontend React Engineer",
        )
    )

    criteria = JobSearchCriteria(
        keywords=[
            "python",
            "django",
        ],
    )

    jobs = repository.search(criteria)

    assert len(jobs) == 2

    ids = {job.id for job in jobs}

    assert ids == {"1", "2"}

def test_repository_searches_by_partial_company_name():

    repository = JobOfferRepository()

    repository.delete_all()

    repository.save(
        create_job_offer(
            id="1",
            company_name="Canonical",
        )
    )

    repository.save(
        create_job_offer(
            id="2",
            company_name="GitLab",
        )
    )

    criteria = JobSearchCriteria(
        company_name="canon",
    )

    jobs = repository.search(criteria)

    assert len(jobs) == 1
    assert jobs[0].company_name == "Canonical"

def test_repository_searches_by_partial_location():

    repository = JobOfferRepository()

    repository.delete_all()

    repository.save(
        create_job_offer(
            id="1",
            location="Málaga, Spain",
        )
    )

    repository.save(
        create_job_offer(
            id="2",
            location="Berlin, Germany",
        )
    )

    criteria = JobSearchCriteria(
        location="Málaga",
    )

    jobs = repository.search(criteria)

    assert len(jobs) == 1
    assert jobs[0].location == "Málaga, Spain"

def test_repository_sorts_by_created_at_descending():

    repository = JobOfferRepository()

    repository.delete_all()

    repository.save(
        create_job_offer(
            id="1",
            created_at=datetime(2026, 1, 1),
        )
    )

    repository.save(
        create_job_offer(
            id="2",
            created_at=datetime(2026, 2, 1),
        )
    )

    criteria = JobSearchCriteria(
        sort_by=JobSortField.CREATED_AT,
    )

    jobs = repository.search(criteria)

    assert jobs[0].id == "2"
    assert jobs[1].id == "1"

def test_repository_searches_by_created_after():

    repository = JobOfferRepository()

    repository.delete_all()

    repository.save(
        create_job_offer(
            id="1",
            created_at=datetime(2026, 1, 1),
        )
    )

    repository.save(
        create_job_offer(
            id="2",
            created_at=datetime(2026, 2, 1),
        )
    )

    criteria = JobSearchCriteria(
        created_after=datetime(2026, 1, 15),
    )

    jobs = repository.search(criteria)

    assert len(jobs) == 1
    assert jobs[0].id == "2"

def test_repository_searches_by_created_before():

    repository = JobOfferRepository()

    repository.delete_all()

    repository.save(
        create_job_offer(
            id="1",
            created_at=datetime(2026, 1, 1),
        )
    )

    repository.save(
        create_job_offer(
            id="2",
            created_at=datetime(2026, 2, 1),
        )
    )

    criteria = JobSearchCriteria(
        created_before=datetime(2026, 1, 15),
    )

    jobs = repository.search(criteria)

    assert len(jobs) == 1
    assert jobs[0].id == "1"
    
def test_repository_persists_salary():

    repository = JobOfferRepository()

    repository.delete_all()

    job = create_job_offer(
        salary=SalaryExpectation(
            amount=70000,
        ),
    )

    repository.save(job)

    loaded = repository.search(
        JobSearchCriteria(),
    )[0]

    assert loaded.salary is not None
    assert loaded.salary.amount == 70000
    assert loaded.salary.currency == "EUR"
    
