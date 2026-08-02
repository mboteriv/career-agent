from career_agent.models.candidate_profile import CandidateProfile
from career_agent.models.enums import RemoteType
from career_agent.models.job_offer import JobOffer
from career_agent.models.match_result import MatchResult
from career_agent.services.job_matching_service import (
    JobMatchingService,
)
from career_agent.services.recommendation_service import RecommendationService
from career_agent.testing.factories import create_job_offer


def test_recommend_returns_one_result_per_job():

    service = RecommendationService()

    profile = CandidateProfile()

    jobs = [
        create_job_offer(),
        create_job_offer(
            id="2",
        ),
    ]

    results = service.recommend(
        jobs,
        profile,
    )

    assert len(results) == 2
    
def test_recommend_returns_results_sorted_by_score():

    service = RecommendationService()

    profile = CandidateProfile(
        preferred_remote_type=RemoteType.REMOTE,
    )

    remote_job = create_job_offer(
        id="1",
        remote_type=RemoteType.REMOTE,
    )

    onsite_job = create_job_offer(
        id="2",
        remote_type=RemoteType.ONSITE,
    )

    results = service.recommend(
        [
            onsite_job,
            remote_job,
        ],
        profile,
    )

    assert results[0].job.id == "1"
    assert results[1].job.id == "2"