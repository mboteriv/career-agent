from career_agent.repositories.semantic_repository import (
    SemanticRepository,
)
from career_agent.models.skill_gap import SkillGap


class SkillGapAnalyzer:

    def __init__(
        self,
        repository: SemanticRepository,
    ):
        self._repository = repository

    def analyze(
        self,
        occupation_id: str,
        candidate_skills: list[str],
    ) -> SkillGap:

        missing_essential = []
        missing_optional = []
        total_essential = 0
        total_optional = 0
        
        for skill in self._repository.find_skills_for_occupation(
            occupation_id,
        ):

            relation_type = self._repository.find_relation_type(
                occupation_id,
                skill.id,
            )

            if relation_type == "essential":

                total_essential += 1

            elif relation_type == "optional":

                total_optional += 1
            
            if skill.id in candidate_skills:
                continue

            if relation_type == "essential":

                missing_essential.append(
                    skill,
                )

            elif relation_type == "optional":

                missing_optional.append(
                    skill,
                )

        return SkillGap(
            missing_essential=missing_essential,
            missing_optional=missing_optional,
            total_essential=total_essential,
            total_optional=total_optional,
        )