from career_agent.models.decision_explanation import (
    DecisionExplanation,
)
from career_agent.models.occupation_match import (
    OccupationMatch,
)


class DecisionExplainer:

    def explain(
        self,
        match: OccupationMatch,
    ) -> DecisionExplanation:

        return DecisionExplanation(
            summary=self._build_summary(match),
            reasons=self._build_reasons(match),
        )
    
    def _missing_skills_reason(
        self,
        skills: list[SemanticEntity],
        skill_type: str,
    ) -> str:

        skill_names = [
            skill.preferred_label
            for skill in skills
        ]

        if len(skill_names) == 1:

            return (
                f"You are missing the {skill_type} skill: "
                f"{skill_names[0]}."
            )

        if len(skill_names) == 2:

            return (
                f"You are missing the {skill_type} skills: "
                f"{skill_names[0]} and {skill_names[1]}."
            )

        skill_list = (
            f"{', '.join(skill_names[:-1])} "
            f"and {skill_names[-1]}"
        )

        return (
            f"You are missing the {skill_type} skills: "
            f"{skill_list}."
        )
    
    def _build_summary(
        self,
        match: OccupationMatch,
    ) -> str:

        occupation = match.occupation.preferred_label

        if match.score == 1.0:
            return f"{occupation} is a strong match."

        if match.score == 0.0:
            return f"{occupation} is not a match."

        return (
            f"{occupation} is a partial match "
            f"({round(match.score * 100)}%)."
        )
        
    def _build_reasons(
        self,
        match: OccupationMatch,
    ) -> list[str]:

        reasons = []

        if match.score == 1.0:

            reasons.append(
                "You have all the essential skills "
                "required for this occupation.",
            )

            if match.skill_gap.missing_optional:

                reasons.append(
                    self._missing_skills_reason(
                        match.skill_gap.missing_optional,
                        "optional",
                    ),
                )

            return reasons

        if match.skill_gap.missing_essential:

            reasons.append(
                self._missing_skills_reason(
                    match.skill_gap.missing_essential,
                    "essential",
                ),
            )

        return reasons