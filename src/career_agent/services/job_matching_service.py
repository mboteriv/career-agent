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
        
        matched = []
        missing = []

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
            self._match_skills(
                job,
                profile,
            ),
            self._match_languages(
                job,
                profile,
            ),
            self._match_experience(
                job,
                profile,
            ),
        ]
        
        matched_requirements=[],
        missing_requirements=[],

        self._merge_explanations(
            matched,
            missing,
            self._explain_remote(
                job,
                profile,
            ),
        )
        
        self._merge_explanations(
            matched,
            missing,
            self._explain_skills(
                job,
                profile,
            ),
        )
        
        self._merge_explanations(
            matched,
            missing,
            self._explain_languages(
                job,
                profile,
            ),
        )
        
        self._merge_explanations(
            matched,
            missing,
            self._explain_experience(
                job,
                profile,
            ),
        )
        
        self._merge_explanations(
            matched,
            missing,
            self._explain_salary(
                job,
                profile,
            ),
        )
        
        skills_matched, skills_missing = self._explain_skills(
            job,
            profile,
        )

        matched.extend(skills_matched)
        missing.extend(skills_missing)
        
        languages_matched, languages_missing = (
            self._explain_languages(
                job,
                profile,
            )
        )
        
        matched.extend(
            languages_matched,
        )
        
        missing.extend(
            languages_missing,
        )
        
        experience_matched, experience_missing = (
            self._explain_experience(
                job,
                profile,
            )
        )

        matched.extend(
        experience_matched,
        )

        missing.extend(
            experience_missing,
        )
        
        salary_matched, salary_missing = self._explain_salary(
            job,
            profile,
        )

        matched.extend(
        salary_matched,
        )

        missing.extend(
        salary_missing,
        )

        return MatchResult(
            job=job,
            score=self._calculate_score(scores),
            matched_requirements=matched,
            missing_requirements=missing,
        )
        
        
        
    def _calculate_score(
        self,
        scores: list[float],
    ) -> float:

        return max(scores)

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
    
    def _match_skills(
        self,
        job: JobOffer,
        profile: CandidateProfile,
    ) -> float:

        required = set(
            job.requirements.skills,
        )

        if not required:
            return 0.0

        candidate = set(
            profile.skills,
        )

        matches = required & candidate

        return len(matches) / len(required)
    
    def _match_languages(
        self,
        job: JobOffer,
        profile: CandidateProfile,
    ) -> float:

        required = {
            language.language
            for language in job.requirements.languages
        }

        if not required:
            return 0.0

        candidate = {
            language.language
            for language in profile.languages
        }

        matches = required & candidate

        return len(matches) / len(required)
    
    def _match_experience(
        self,
        job: JobOffer,
        profile: CandidateProfile,
    ) -> float:

        if job.requirements.years_experience is None:
            return 0.0

        if profile.years_experience is None:
            return 0.0

        if profile.years_experience >= job.requirements.years_experience:
            return 1.0

        return 0.0
    
    def _explain_remote(
        self,
        job: JobOffer,
        profile: CandidateProfile,
    ) -> tuple[list[str], list[str]]:
        if profile.preferred_remote_type is None:
            return [], []

        if profile.preferred_remote_type == job.remote_type:
            return ["Remote"], []

        return [], ["Remote"]
    
    def _explain_skills(
        self,
        job: JobOffer,
        profile: CandidateProfile,
    ) -> tuple[list[str], list[str]]:
        required = set(job.requirements.skills)
        candidate = set(profile.skills)

        matched = list(required & candidate)
        missing = list(required - candidate)

        return matched, missing
    
    def _explain_languages(
        self,
        job: JobOffer,
        profile: CandidateProfile,
    ) -> tuple[list[str], list[str]]:
        required = {
            language.language
            for language in job.requirements.languages
        }

        candidate = {
            language.language
            for language in profile.languages
        }


        matched = list(required & candidate)
        missing = list(required - candidate)

        return matched, missing
    
    def _explain_experience(
        self,
        job: JobOffer,
        profile: CandidateProfile,
    ) -> tuple[list[str], list[str]]:

        if job.requirements.years_experience is None:
            return [], []

        if profile.years_experience >= job.requirements.years_experience:
            return ["Experience"], []

        return [], ["Experience"]
    
    def _explain_salary(
        self,
        job: JobOffer,
        profile: CandidateProfile,
    ) -> tuple[list[str], list[str]]:

        if job.salary is None:
            return [], []

        if profile.salary is None:
            return [], []

        if job.salary.amount >= profile.salary.amount:
            return ["Salary"], []

        return [], ["Salary"]
    
    def _merge_explanations(
        self,
        matched: list[str],
        missing: list[str],
        explanation: tuple[list[str], list[str]],
    ) -> None:

        matched_items, missing_items = explanation

        matched.extend(
            matched_items,
        )

        missing.extend(
            missing_items,
        )
