from career_agent.models.job_search_criteria import JobSearchCriteria
from career_agent.repositories.job_offer_repository import JobOfferRepository
from career_agent.services.job_search_service import JobSearchService
from tests.factories import create_job_offer

def test_search_returns_matching_jobs():

    repository = JobOfferRepository()
    repository.delete_all()

    repository.save(
        create_job_offer(
            company_name="Canonical",
        )
    )

    service = JobSearchService(
        repository=repository,
    )

    jobs = service.search(
        JobSearchCriteria(
            company_name="Canonical",
        )
    )

    assert len(jobs) == 1