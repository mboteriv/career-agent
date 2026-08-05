import profile

from career_agent.models.candidate_profile import (
    CandidateProfile,
)
from career_agent.models.criterion_match import CriterionMatch
from career_agent.models.matching_criterion import MatchingCriterion
from career_agent.models.job_offer import JobOffer
from career_agent.models.match_result import MatchResult
from career_agent.services.matching_score_calculator import MatchingScoreCalculator
from career_agent.models.matching_policy import MatchingPolicy


class JobMatchingService:
    
    def __init__(self):

        self._score_calculator = MatchingScoreCalculator()

    def match(
        self,
        job: JobOffer,
        profile: CandidateProfile,
    ) -> MatchResult:
        
        matched = []
        missing = []

        criterion_matches = self._build_criterion_matches(
            job,
            profile,
        )

        matched, missing = self._build_explanations(
        job,
        profile,
        criterion_matches,
        )
        
        return self._build_match_result(
            job,
            criterion_matches,
            matched,
            missing,
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
    
    def _match_skills(
        self,
        job: JobOffer,
        profile: CandidateProfile,
    ) -> float:

        required, matched = self._skill_matches(
            job,
            profile,
        )

        if not required:
            return 0.0

        return len(
            matched,
        ) / len(
            required,
        )
    
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
    
    def _build_criterion_matches(
        self,
        job: JobOffer,
        profile: CandidateProfile,
    ) -> list[CriterionMatch]:

        return [
            CriterionMatch(
                criterion=MatchingCriterion.REMOTE,
                score=self._match_remote(
                    job,
                    profile,
                ),
                applicable=(
                    profile.preferred_remote_type
                    is not None
                ),
            ),
            CriterionMatch(
                criterion=MatchingCriterion.COUNTRY,
                score=self._match_country(
                    job,
                    profile,
                ),
                applicable=bool(
                    profile.preferred_countries,
                ),
            ),
            CriterionMatch(
                criterion=MatchingCriterion.SALARY,
                score=self._match_salary(
                    job,
                    profile,
                ),
                applicable=(
                    profile.salary is not None
                    and job.salary is not None
                ),
            ),
            self._build_skills_criterion_match(
                job,
                profile,
            ),
            CriterionMatch(
                criterion=MatchingCriterion.LANGUAGES,
                score=self._match_languages(
                    job,
                    profile,
                ),
                applicable=bool(
                    job.requirements.languages,
                ),
            ),
            CriterionMatch(
                criterion=MatchingCriterion.EXPERIENCE,
                score=self._match_experience(
                    job,
                    profile,
                ),
                applicable=(
                    job.requirements.years_experience
                    is not None
                ),
            ),
        ]
    
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
        
    def _skill_matches(
        self,
        job: JobOffer,
        profile: CandidateProfile,
    ) -> tuple[
        set[str],
        set[str],
    ]:

        required = set(
            job.requirements.skills,
        )

        candidate = set(
            profile.skills,
        )

        matched = required & candidate

        return (
            required,
            matched,
    )
        
    def _build_skills_criterion_match(
            self,
            job: JobOffer,
            profile: CandidateProfile,
        ) -> CriterionMatch:

            applicable = bool(job.requirements.skills)
    
            required, matched = self._skill_matches(
                job,
                profile,
            )

            missing = required - matched

            return CriterionMatch(
                criterion=MatchingCriterion.SKILLS,
                score=self._match_skills(
                job,
                profile,
            ),
            matched=list(matched),
            missing=list(missing),
            applicable=applicable,
        )
            
    def _build_explanations(
        self,
        job: JobOffer,
        profile: CandidateProfile,
        criterion_matches: list[CriterionMatch],
    ) -> tuple[
        list[str],
        list[str],
    ]:

        matched = []
        missing = []

        self._merge_explanations(
            matched,
            missing,
            self._explain_remote(
                job,
                profile,
            ),
         )

        skills = self._find_criterion_match(
            criterion_matches,
            MatchingCriterion.SKILLS,
        )

        matched.extend(
            skills.matched,
        )

        missing.extend(
            skills.missing,
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

        return (
            matched,
            missing,
        )
        
    def _build_match_result(
        self,
        job: JobOffer,
        criterion_matches: list[CriterionMatch],
        matched: list[str],
        missing: list[str],
    ) -> MatchResult:

        scores = [
            criterion.score
            for criterion
            in criterion_matches
        ]

        return MatchResult(
            job=job,
            score=self._score_calculator.calculate(
                criterion_matches,
                MatchingPolicy(),
        ),
            matched_requirements=matched,
            missing_requirements=missing,
        )
        
    def _find_criterion_match(
        self,
        criterion_matches,
        criterion,
    ):

        for match in criterion_matches:

            if match.criterion == criterion:
                return match

        raise ValueError(
            f"Unknown criterion: {criterion}",
        )
        
    
