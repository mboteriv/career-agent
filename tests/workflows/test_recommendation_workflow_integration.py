from career_agent.models.recommendation_options import (
    RecommendationOptions,
)
from career_agent.repositories.candidate_profile_repository import (
    CandidateProfileRepository,
)
from career_agent.repositories.job_offer_repository import (
    JobOfferRepository,
)
from career_agent.workflows.recommendation_workflow import (
    RecommendationWorkflow,
)
from tests.factories import (
    create_candidate_profile,
    create_job_offer,
)
from career_agent.models.matching_policy import MatchingPolicy


def test_workflow_recommends_jobs_from_persisted_data():

    profile_repository = CandidateProfileRepository(
        "test_profile.json",
    )

    job_repository = JobOfferRepository()

    profile_repository.delete()
    job_repository.delete_all()

    profile_repository.save(
        create_candidate_profile(
            skills=[
                "Python",
            ],
        ),
    )

    job_repository.save(
        create_job_offer(
            description="Python required.",
        ),
    )

    workflow = RecommendationWorkflow(
        profile_repository=profile_repository,
        job_repository=job_repository,
    )

    results = workflow.execute(
        RecommendationOptions(),
    )

    assert len(results) == 1
    assert results[0].job.title == "Backend Engineer"

    profile_repository.delete()
    job_repository.delete_all()