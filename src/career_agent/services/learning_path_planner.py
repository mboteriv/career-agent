from career_agent.models.learning_path import LearningPath

from career_agent.models.skill_dependency import SkillDependency
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
        dependencies = []
        
        for recommendation in recommendations.recommendations:

            steps.extend(
                self._collect_prerequisites(
                    recommendation.skill,
                    recommendation.priority,
                    visited,
                    dependencies,
                )
            )

            if recommendation.skill.id not in visited:

                visited.add(
                    recommendation.skill.id,
                )

                steps.append(
                    recommendation,
                )
                
        print("DEPENDENCIES:", dependencies)
                               
        return LearningPath(
            steps=steps,
            dependencies=dependencies,
        )
        
    def _collect_prerequisites(
        self,
        skill: SemanticEntity,
        priority: RecommendationPriority,
        visited: set[str] | None = None,
        dependencies: list[SkillDependency] | None = None,
    ) -> list[SkillRecommendation]:
        
        if visited is None:
            visited = set()
            
        if dependencies is None:
            dependencies = []
        
        prerequisites = self._repository.find_prerequisites(
            skill.id,
        )

        if not prerequisites:
            return []
        steps = []

        for prerequisite in prerequisites:

            if prerequisite.id in visited:
                dependency = SkillDependency(
                    prerequisite_skill_id=prerequisite.id,
                    dependent_skill_id=skill.id,
                )

                if dependency not in dependencies:
                    dependencies.append(
                        dependency,
                    )

                continue

            visited.add(
                prerequisite.id,
            )

            steps.extend(
                self._collect_prerequisites(
                    prerequisite,
                    priority,
                    visited,
                    dependencies,
                )
            )

            dependency = SkillDependency(
                prerequisite_skill_id=prerequisite.id,
                dependent_skill_id=skill.id,
            )

            if dependency not in dependencies:
                dependencies.append(
                    dependency,
                )

            steps.append(
                SkillRecommendation(
                    skill=prerequisite,
                    priority=priority,
                )
            )

        return steps