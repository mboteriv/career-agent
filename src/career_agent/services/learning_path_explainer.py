from career_agent.models.learning_path import LearningPath
from career_agent.models.learning_path_explanation import (
    LearningPathExplanation,
)
from career_agent.models.recommendation_priority import RecommendationPriority


class LearningPathExplainer:

    def explain(
        self,
        learning_path: LearningPath,
        dependencies: list[SkillDependency] | None = None,
    ) -> LearningPathExplanation:
        
        if dependencies is None:
            dependencies = learning_path.dependencies

        if not learning_path.steps:

            return LearningPathExplanation(
                summary="No skills are included in the learning path.",
                reasons=[],
            )
        reasons = self._build_dependency_reasons(
            learning_path,
            dependencies,
        )
            
        total = len(learning_path.steps)

        if total == 1:

            step = learning_path.steps[0]

            return LearningPathExplanation(
                summary=(
                    f"Learning path with 1 skill: "
                    f"{step.skill.preferred_label} "
                    f"({self._format_priority(step.priority)})."
                ),
                reasons=reasons,
            )

        return LearningPathExplanation(
            summary=(
                f"Learning path with {total} skills: "
                f"{self._format_steps(learning_path.steps)}."
            ),
            reasons=reasons,
        )
        
    def _format_priority(
        self,
        priority: RecommendationPriority,
    ) -> str:

        if priority == RecommendationPriority.ESSENTIAL:
            return "essential"

        return "optional"
    
    def _format_steps(
        self,
        steps: list[SkillRecommendation],
    ) -> str:

        formatted_steps = [
            (
                f"{step.skill.preferred_label} "
                f"({self._format_priority(step.priority)})"
            )
            for step in steps
        ]

        if len(formatted_steps) == 2:

            return (
                f"{formatted_steps[0]} "
                f"and {formatted_steps[1]}"
            )

        return (
            f"{', '.join(formatted_steps[:-1])} "
            f"and {formatted_steps[-1]}"
        )
        
    def _build_dependency_reasons(
        self,
        learning_path: LearningPath,
        dependencies: list[SkillDependency],
    ) -> list[str]:
        
        step_ids = {
            step.skill.id
            for step in learning_path.steps
        }

        labels = {
            step.skill.id: step.skill.preferred_label
            for step in learning_path.steps
        }

        step_positions = {
            step.skill.id: index
            for index, step in enumerate(learning_path.steps)
        }

        relevant_dependencies = []
        seen_dependencies = set()

        for dependency in dependencies:
            
            if dependency.dependent_skill_id not in step_ids:
                continue

            dependency_key = (
                dependency.prerequisite_skill_id,
                dependency.dependent_skill_id,
            )

            if dependency_key in seen_dependencies:
                continue

            seen_dependencies.add(
                dependency_key,
            )
            
            relevant_dependencies.append(
                dependency,
            )

        relevant_dependencies.sort(
            key=lambda dependency: step_positions.get(
                dependency.dependent_skill_id,
                float("inf"),
            ),
        )
        
        reasons = []
        
        for dependency in relevant_dependencies:
            
            prerequisite_label = labels.get(
                dependency.prerequisite_skill_id,
                dependency.prerequisite_skill_id,
            )

            dependent_label = labels.get(
                dependency.dependent_skill_id,
                dependency.dependent_skill_id,
            )

            reasons.append(
                f"{prerequisite_label} should be learned before "
                f"{dependent_label} because it is a prerequisite."
            )

        return reasons