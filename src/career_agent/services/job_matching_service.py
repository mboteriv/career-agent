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
from career_agent.models.language_levels import (
    LANGUAGE_LEVELS,
)


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

        matched, missing = (
            self._build_requirements_summary(
            criterion_matches,
            )
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

        return self._match_ratio(
            required,
            matched,
        )
    
    def _match_languages(
        self,
        job: JobOffer,
        profile: CandidateProfile,
    ) -> float:

        required, matched = self._language_matches(
            job,
            profile,
        )

        return self._match_ratio(
            required,
            matched,
        )
    
    def _match_experience(
        self,
        job: JobOffer,
        profile: CandidateProfile,
    ) -> float:

        required = job.requirements.years_experience

        if required is None:
            return 0.0

        if profile.years_experience is None:
            return 0.0

        if required == 0:
            return 1.0

        return min(
            profile.years_experience / required,
            1.0,
        )
    
    def _build_criterion_matches(
        self,
        job: JobOffer,
        profile: CandidateProfile,
    ) -> list[CriterionMatch]:

        return [
            self._build_remote_criterion_match(
                job,
                profile,
            ),
            self._build_country_criterion_match(
                job,
                profile,
            ),
            self._build_salary_criterion_match(
                job,
                profile,
            ),
            self._build_skills_criterion_match(
                job,
                profile,
            ),
            self._build_languages_criterion_match(
                job,
                profile,
            ),
            self._build_experience_criterion_match(
                job,
                profile,
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

            score = self._match_ratio(
                required,
                matched,
            )

            return CriterionMatch(
                criterion=MatchingCriterion.SKILLS,
                score=score,
                matched=sorted(matched),
                missing=sorted(missing),
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
            criterion_matches=criterion_matches,
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
        
    def _build_requirements_summary(
        self,
        criterion_matches: list[CriterionMatch],
    ) -> tuple[
        list[str],
        list[str],
    ]:
        matched = []
        missing = []

        for criterion_match in criterion_matches:

            matched.extend(
                criterion_match.matched
            )

            missing.extend(
                criterion_match.missing
            )

        return (
            matched,
            missing,
        )
            
    def _build_remote_criterion_match(
        self,
        job: JobOffer,
        profile: CandidateProfile,
    ) -> CriterionMatch:
                
        score = self._match_remote(
            job,
            profile,
        )
        
        applicable = (
            profile.preferred_remote_type
            is not None
        )
        
        matched = []
        missing = []

        if applicable:

            if score == 1.0:
                matched.append(
                    "Remote",
                )
            else:
                missing.append(
                    "Remote",
                )

        return CriterionMatch(
            criterion=MatchingCriterion.REMOTE,
            score=score,
            applicable=applicable,
            matched=matched,
            missing=missing,
        )
        
    def _build_country_criterion_match(
        self,
        job: JobOffer,
        profile: CandidateProfile,
    ) -> CriterionMatch:

        score = self._match_country(
            job,
            profile,
        )

        applicable = bool(
            profile.preferred_countries,
        )

        matched = []
        missing = []

        if applicable:

            if score == 1.0:
                matched.append(
                    "Country",
                )
            else:
                missing.append(
                    "Country",
                )

        return CriterionMatch(
            criterion=MatchingCriterion.COUNTRY,
            score=score,
            applicable=applicable,
            matched=matched,
            missing=missing,
        )
        
    def _build_salary_criterion_match(
        self,
        job: JobOffer,
        profile: CandidateProfile,
    ) -> CriterionMatch:

        score = self._match_salary(
            job,
            profile,
        )

        applicable = (
            profile.salary is not None
            and job.salary is not None
        )
        
        details = {}

        if (
            profile.salary is not None
            and job.salary is not None
        ):
            details = {
                "candidate": profile.salary.amount,
                "required": job.salary.amount,
                "currency": job.salary.currency,
            }

        matched = []
        missing = []

        if applicable:

            if score == 1.0:
                matched.append(
                    "Salary",
                )
            else:
                missing.append(
                    "Salary",
                )

        return CriterionMatch(
            criterion=MatchingCriterion.SALARY,
            score=score,
            applicable=applicable,
            matched=matched,
            missing=missing,
            details=details,
        )
        
    def _build_languages_criterion_match(
        self,
        job: JobOffer,
        profile: CandidateProfile,
    )-> CriterionMatch:
        
        details = {}

        if profile.languages and job.requirements.languages:

            candidate = profile.languages[0]
            required = job.requirements.languages[0]

            details = {
                "candidate": (
                    f"{candidate.language} {candidate.level}"
                ),
                "required": (
                    f"{required.language} {required.level}"
                ),
            }

        applicable = bool(
            job.requirements.languages,
        )

        required, matched = self._language_matches(
            job,
            profile,
        )

        missing = required - matched

        score = self._match_ratio(
            required,
            matched,
        )

        return CriterionMatch(
            criterion=MatchingCriterion.LANGUAGES,
            score=score,
            matched=sorted(matched),
            missing=sorted(missing),
            applicable=applicable,
            details=details,
        )
    
    def _build_experience_criterion_match(
        self,
        job: JobOffer,
        profile: CandidateProfile,
    ) -> CriterionMatch:

        score = self._match_experience(
            job,
            profile,
        )

        applicable = (
            job.requirements.years_experience
            is not None
        )
        
        details={
            "required": (
                job.requirements.years_experience
            ),
            "candidate": (
                profile.years_experience
            ),
        }

        matched = []
        missing = []

        if applicable:

            if score == 1.0:
                matched.append(
                    "Experience",
                )
            else:
                missing.append(
                    "Experience",
                )

        return CriterionMatch(
            criterion=MatchingCriterion.EXPERIENCE,
            score=score,
            applicable=applicable,
            matched=matched,
            missing=missing,
            details=details,
        )
        
    def _language_matches(
        self,
        job: JobOffer,
        profile: CandidateProfile,
    ) -> tuple[
        set[str],
        set[str],
    ]:
        candidate_languages = self._candidate_languages(
            profile,
        )

        required = set()
        matched = set()

        for language in job.requirements.languages:

            required.add(
                language.language,
            )

            candidate_level = candidate_languages.get(
                language.language,
            )

            if candidate_level is None:
                continue

            if self._language_level_matches(
                candidate_level,
                language.level,
            ):
                matched.add(
                    language.language,
                )

        return (
            required,
            matched,
        )
        
    def _match_ratio(
        self,
        required: set[str],
        matched: set[str],
    ) -> float:

        if not required:
            return 0.0

        return len(matched) / len(required)
    
    def _language_level_matches(
        self,
        candidate_level: str,
        required_level: str,
    ) -> bool:

        candidate = LANGUAGE_LEVELS.get(
            candidate_level,
        )

        required = LANGUAGE_LEVELS.get(
            required_level,
        )

        if (
            candidate is None
            or required is None
        ):
            return False

        return candidate >= required
    
    def _candidate_languages(
        self,
        profile: CandidateProfile,
    ) -> dict[str, str]:

        return {
            language.language: language.level
            for language
            in profile.languages
        }
        
    
