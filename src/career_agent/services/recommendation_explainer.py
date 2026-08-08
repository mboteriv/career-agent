from career_agent.models.recommendation_explanation import (
    RecommendationExplanation,
)
from career_agent.models.recommendation_priority import RecommendationPriority
from career_agent.models.skill_recommendation import (
    SkillRecommendation,
)
from career_agent.models.skill_recommendation import (
    RecommendationPriority,
    SkillRecommendation,
)
from career_agent.models.skill_recommendation_result import SkillRecommendationResult



class RecommendationExplainer:

    def explain(
        self,
        recommendation: SkillRecommendation,
    ) -> RecommendationExplanation:

        if recommendation.priority == RecommendationPriority.ESSENTIAL:

            return RecommendationExplanation(
                summary=(
                    f"{recommendation.skill.preferred_label} "
                    "is an essential skill to learn."
                ),
                reasons=[
                    "This skill is essential for the target occupation.",
                    "This skill is missing from your current skills.",
                ],
            )

        return RecommendationExplanation(
            summary=(
                f"{recommendation.skill.preferred_label} "
                "is an optional skill to learn."
            ),
            reasons=[
                "This skill is optional for the target occupation.",
                "This skill is missing from your current skills.",
            ],
        )
    
    def explain_result(
        self,
        result: SkillRecommendationResult,
    ) -> RecommendationExplanation:

        recommendations = result.recommendations
        
        if not recommendations:

            return RecommendationExplanation(
                summary="No skills are recommended.",
                reasons=[],
            )

        total = len(recommendations)

        if total == 1:

            recommendation = recommendations[0]
            
            recommendation_explanation = self.explain(
                recommendation,
            )

            return RecommendationExplanation(
                summary=(
                    f"1 skill is recommended: "
                    f"{recommendation.skill.preferred_label} "
                    f"({self._format_priority(recommendation.priority)})."
                ),
                reasons=recommendation_explanation.reasons,
            )
        
        reasons=self._collect_reasons(recommendations)

        return RecommendationExplanation(
            summary=(
                f"{total} skills are recommended: "
                f"{self._format_recommendations(recommendations)}."
            ),
            reasons=reasons,
        )
        
    def _collect_reasons(
        self,
        recommendations: list[SkillRecommendation],
    ) -> list[str]:

        reasons = []

        for recommendation in recommendations:

            explanation = self.explain(
                recommendation,
            )

            reasons.extend(
                explanation.reasons,
            )

        return reasons
    
    def _format_priority(
        self,
        priority: RecommendationPriority,
    ) -> str:

        if priority == RecommendationPriority.ESSENTIAL:
            return "essential"

        return "optional"
    
    def _format_recommendations(
        self,
        recommendations: list[SkillRecommendation],
    ) -> str:

        formatted_recommendations = [
            (
                f"{recommendation.skill.preferred_label} "
                f"({self._format_priority(recommendation.priority)})"
            )
            for recommendation in recommendations
        ]

        if len(formatted_recommendations) == 2:

            return (
                f"{formatted_recommendations[0]} "
                f"and {formatted_recommendations[1]}"
            )

        return (
            f"{', '.join(formatted_recommendations[:-1])} "
            f"and {formatted_recommendations[-1]}"
        )