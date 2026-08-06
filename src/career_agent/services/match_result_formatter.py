from career_agent.models.criterion_match import CriterionMatch
from career_agent.models.match_result import MatchResult
from career_agent.models.matching_criterion import MatchingCriterion
from career_agent.models.matching_policy import MatchingPolicy


class MatchResultFormatter:

    def format(
        self,
        result: MatchResult,
    ) -> str:

        lines = []

        lines.extend(
            self._format_score(
                result,
            ),
        )

             
        lines.extend(
            self._format_criteria(
                result,
            ),
        )

        return "\n".join(lines)
    
    def _format_missing(
        self,
        result: MatchResult,
    ) -> list[str]:

        if not result.missing_requirements:
            return []

        lines = []

        lines.append("")
        lines.append("Missing")

        for requirement in result.missing_requirements:

            lines.append(
                f"✗ {requirement}"
            )

        return lines
    
    def _format_score(
        self,
        result: MatchResult,
    ) -> list[str]:

        return [
            f"Overall match: {result.score:.0%}",
        ]
        
    def _format_matched(
        self,
        result: MatchResult,
    )-> list[str]:

        if not result.matched_requirements:
            return []

        lines = []

        lines.append("")
        lines.append("Matched")

        for requirement in result.matched_requirements:

            lines.append(
                f"✓ {requirement}"
            )

        return lines
    
    def _format_criteria(
        self,
        result: MatchResult,
    ) -> list[str]:
        
        if not result.criterion_matches:
            return []

        lines = []

        lines.append("")
        lines.append("Criteria")

        for criterion in self._sorted_criteria(
            result,
        ):

            if not criterion.applicable:
                continue

            lines.extend(
                self._format_criterion(
                    criterion,
                ),
            )

        return lines
    
    def _format_criterion(
        self,
        criterion: CriterionMatch,
    ) -> list[str]:

        match criterion.criterion:

            case MatchingCriterion.EXPERIENCE:
                return self._format_experience(
                    criterion,
                )
                
            case MatchingCriterion.SALARY:
                return self._format_salary(
                    criterion,
                )
                
            case MatchingCriterion.LANGUAGES:
                return self._format_languages(
                criterion,
            )

            case _:
                return self._format_default(
                    criterion,
                )
            
    
    def _sorted_criteria(
        self,
        result: MatchResult,
    ) -> list[CriterionMatch]:
        
        policy = MatchingPolicy()

        return sorted(
            (
                criterion
                for criterion
                in result.criterion_matches
                if criterion.applicable
            ),
            key=lambda criterion:
                policy.weight_for(
                    criterion.criterion,
                ),
            reverse=True,
        )
        
    def _format_default(
        self,
        criterion: CriterionMatch,
    ) -> list[str]:

        lines = [
            (
                f"{criterion.criterion.value.title()}: "
                f"{criterion.score:.0%}"
            ),
        ]

        for requirement in criterion.matched:
            lines.append(
                f"  ✓ {requirement}"
            )   

        for requirement in criterion.missing:
            lines.append(
                f"  ✗ {requirement}"
            )

        lines.append("")

        return lines
    
    def _format_experience(
        self,
        criterion: CriterionMatch,
    ) -> list[str]:

        lines = self._format_default(
            criterion,
        )

        lines.insert(
            1,
            (
                "  Candidate: "
                f"{criterion.details['candidate']} years"
            ),
        )

        lines.insert(
            2,
            (
                "  Required: "
                f"{criterion.details['required']} years"
            ),
        )

        return lines
    
    def _format_salary(
        self,
        criterion: CriterionMatch,
    ) -> list[str]:

        lines = self._format_default(
            criterion,
        )

        candidate = criterion.details.get(
            "candidate",
        )

        required = criterion.details.get(
            "required",
        )

        currency = criterion.details.get(
            "currency",
            "",
        )

        lines.insert(
            1,
            f"  Candidate: {candidate} {currency}",
        )

        lines.insert(
            2,
            f"  Required: {required} {currency}",
        )

        return lines
    
    def _format_languages(
        self,
        criterion: CriterionMatch,
    ) -> list[str]:

        lines = self._format_default(
            criterion,
        )

        candidate = criterion.details.get(
            "candidate",
        )

        required = criterion.details.get(
            "required",
        )

        lines.insert(
            1,
            f"  Candidate: {candidate}",
        )

        lines.insert(
            2,
            f"  Required: {required}",
        )

        return lines