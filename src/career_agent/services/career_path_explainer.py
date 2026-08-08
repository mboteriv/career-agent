

from career_agent.models.career_path_explanation import CareerPathExplanation


class CareerPathExplainer:

    def explain(
        self,
        career_path: CareerPath,
    ) -> CareerPathExplanation:

        return CareerPathExplanation(
            summary=self._build_summary(
                career_path,
            ),
            reasons=self._build_reasons(
                career_path,
            ),
        )
    def _build_summary(
        self,
        career_path: CareerPath,
    ) -> str:

        if not career_path.occupations:
            return "No occupations were found."

        first = career_path.occupations[0]

        if len(career_path.occupations) == 1:
            return (
                f"{first.occupation.preferred_label} "
                f"is the strongest match."
            )

        second = career_path.occupations[1]

        first_missing = (
            len(first.skill_gap.missing_essential)
            + len(first.skill_gap.missing_optional)
        )

        second_missing = (
            len(second.skill_gap.missing_essential)
            + len(second.skill_gap.missing_optional)
        )

        if first_missing < second_missing:
            return (
                f"{first.occupation.preferred_label} appears before "
                f"{second.occupation.preferred_label} because it "
                f"requires fewer additional skills."
            )

        if first.score > second.score:
            return (
                f"{first.occupation.preferred_label} appears before "
                f"{second.occupation.preferred_label} because "
                f"it is a stronger match."
            )

        return (
            f"{first.occupation.preferred_label} appears before "
            f"{second.occupation.preferred_label}."
        )
    
    def _build_reasons(
        self,
        career_path: CareerPath,
    ) -> list[str]:

        if not career_path.occupations:
            return []

        reasons = []

        for match in career_path.occupations[:2]:

            missing = len(
                match.skill_gap.missing_essential,
            )

            reasons.append(
                f"{match.occupation.preferred_label} requires "
                f"{missing} additional essential skill"
                f"{'s' if missing != 1 else ''}."
            )

        if len(career_path.occupations) < 2:
            return reasons

        first = career_path.occupations[0]
        second = career_path.occupations[1]

        first_missing = (
            len(first.skill_gap.missing_essential)
            + len(first.skill_gap.missing_optional)
        )

        second_missing = (
            len(second.skill_gap.missing_essential)
            + len(second.skill_gap.missing_optional)
        )

        if (
            first_missing >= second_missing
            and first.score > second.score
        ):

            reasons.extend(
                [
                    (
                        f"{first.occupation.preferred_label} "
                        f"has a match score of "
                        f"{round(first.score * 100)}%."
                    ),
                    (
                        f"{second.occupation.preferred_label} "
                        f"has a match score of "
                        f"{round(second.score * 100)}%."
                    ),
                ]
            )

        return reasons
    
