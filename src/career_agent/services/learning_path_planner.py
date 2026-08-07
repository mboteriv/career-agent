from career_agent.models.learning_path import LearningPath

from career_agent.models.skill_recommendation import SkillRecommendation
from career_agent.repositories.semantic_repository import SemanticRepository
from career_agent.services.skill_recommendation_engine import (
    SkillRecommendationEngine,
)


class LearningPathPlanner:

    def __init__(
        self,
        engine: SkillRecommendationEngine,
        repository: SemanticRepository,
    ):
        self._engine = engine
        self._repository = repository
        
    def plan(
        self,
        occupation_id: str,
        candidate_skills: list[str],
    ) -> LearningPath:
        
        recommendations = self._engine.recommend_skills(
            occupation_id,
            candidate_skills,
        )

        steps = []

        visited = set()

        for recommendation in recommendations.recommendations:

            steps.extend(
                self._collect_prerequisites(
                    recommendation.skill,
                    recommendation.priority,
                    visited,
                )
            )

            if recommendation.skill.id not in visited:

                visited.add(
                    recommendation.skill.id,
                )

                steps.append(
                    recommendation,
                )
        return LearningPath(
            steps=steps,
        )
        
    def _collect_prerequisites(
        self,
        skill: SemanticEntity,
        priority: RecommendationPriority,
        visited: set[str] | None = None,
    ) -> list[SkillRecommendation]:
        
        if visited is None:
            visited = set()
        
        prerequisites = self._repository.find_prerequisites(
            skill.id,
        )

        if not prerequisites:
            return []
        steps = []

        for prerequisite in prerequisites:

            if prerequisite.id in visited:
                continue

            visited.add(
                prerequisite.id,
            )

            steps.extend(
                self._collect_prerequisites(
                    prerequisite,
                    priority,
                    visited,
                )
            )

            steps.append(
                SkillRecommendation(
                    skill=prerequisite,
                    priority=priority,
                )
            )

        return steps