from pydantic import BaseModel, ConfigDict, Field

from career_agent.models.skill_recommendation import (
    SkillRecommendation,
)


class SkillRecommendationResult(BaseModel):

    model_config = ConfigDict(
        frozen=True,
    )

    recommendations: list[SkillRecommendation] = Field(
        default_factory=list,
    )