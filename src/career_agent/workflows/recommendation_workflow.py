from career_agent.repositories.candidate_profile_repository import (
    CandidateProfileRepository,
)
from career_agent.repositories.job_offer_repository import (
    JobOfferRepository,
)
from career_agent.services.recommendation_service import (
    RecommendationService,
)
from career_agent.models.job_search_criteria import (
    JobSearchCriteria,
)

class RecommendationWorkflow:

    def __init__(
        self,
        profile_repository=None,
        job_repository=None,
        recommendation_service=None,
    ):

        self._profile_repository = (
            profile_repository
            or CandidateProfileRepository()
        )

        self._job_repository = (
            job_repository
            or JobOfferRepository()
        )

        self._recommendation_service = (
            recommendation_service
            or RecommendationService()
        )
    
    def execute(
        self,
        options: RecommendationOptions,
    ):

        profile = self._profile_repository.load()

        jobs = self._job_repository.search(
            JobSearchCriteria(),
        )

        results = self._recommendation_service.recommend(
            jobs,
            profile,
        )

        results = self._filter_by_score(
            results,
            options,
        )

        results = self._limit_results(
            results,
            options,
        )

        return results
    
    def _filter_by_score(
        self,
        results,
        options: RecommendationOptions,
    ):

        if options.min_score is None:
            return results

        return [
            result
            for result in results
            if result.score >= options.min_score
        ]
        
    def _limit_results(
        self,
        results,
        options: RecommendationOptions,
    ):

        if options.limit is None:
            return results

        return results[
            : options.limit
        ]