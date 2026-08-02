import profile

from career_agent.models.candidate_profile import (
    CandidateProfile,
)
from career_agent.models.job_offer import JobOffer
from career_agent.models.match_result import MatchResult


class JobMatchingService:

    def match(
        self,
        job: JobOffer,
        profile: CandidateProfile,
    ) -> MatchResult:

        scores = [
            self._match_remote(
                job,
                profile,
            ),
            self._match_country(
                job,
                profile,
            ),
            self._match_salary(
                job,
                profile,
            ),
        ]

        return MatchResult(
            score=max(scores),
        )
            
    def _match_remote(
        self,
        job: JobOffer,
        profile: CandidateProfile,
    ) -> float:

        if profile.preferred_remote_type is None:
            return 0.0

        if profile.preferred_remote_type == job.remote_type:
            return 1.0

        return 0.0
    
    def _match_country(
        self,
        job: JobOffer,
        profile: CandidateProfile,
    ) -> float:

        if not profile.preferred_countries:
            return 0.0

        location = job.location.lower()

        for country in profile.preferred_countries:
            if country.lower() in location:
                return 1.0

        return 0.0
    
    def _match_salary(
        self,
        job: JobOffer,
        profile: CandidateProfile,
    ) -> float:

        if profile.salary is None:
            return 0.0

        if job.salary is None:
            return 0.0

        if job.salary.amount >= profile.salary.amount:
            return 1.0

        return 0.0
