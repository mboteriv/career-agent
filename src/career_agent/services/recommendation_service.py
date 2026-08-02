from career_agent.models.candidate_profile import CandidateProfile
from career_agent.models.job_offer import JobOffer
from career_agent.models.match_result import MatchResult
from career_agent.services.job_matching_service import (
    JobMatchingService,
)


class RecommendationService:

    def __init__(self):

        self._matching = JobMatchingService()

    def recommend(
        self,
        jobs: list[JobOffer],
        profile: CandidateProfile,
    ) -> list[MatchResult]:

        results = [
            self._matching.match(
                job,
                profile,
            )
            for job in jobs
        ]
        
        results.sort(
            key=lambda result: result.score,
            reverse=True,
        )

        return results