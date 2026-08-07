from career_agent.models.recommendation_priority import RecommendationPriority
from career_agent.services.skill_gap_analyzer import (
    SkillGapAnalyzer,
)
from career_agent.models.skill_recommendation import (
    SkillRecommendation,
)
from career_agent.models.skill_recommendation_result import (
    SkillRecommendationResult,
)


class SkillRecommendationEngine:

    def __init__(
        self,
        analyzer: SkillGapAnalyzer,
    ):
        self._analyzer = analyzer
        
    def recommend_skills(
        self,
        occupation_id: str,
        candidate_skills: list[str],
    ) -> SkillRecommendationResult:

        gap = self._analyzer.analyze(
            occupation_id,
            candidate_skills,
        )

        recommendations = []

        for skill in gap.missing_essential:

            recommendations.append(
                SkillRecommendation(
                    skill=skill,
                    priority=RecommendationPriority.ESSENTIAL,
                ),
            )
        
        for skill in gap.missing_optional:

            recommendations.append(
                SkillRecommendation(
                    skill=skill,
                    priority=RecommendationPriority.OPTIONAL,
                ),
            )

        return SkillRecommendationResult(
            recommendations=recommendations,
        )