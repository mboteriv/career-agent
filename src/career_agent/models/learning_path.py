from pydantic import BaseModel, ConfigDict, Field

from career_agent.models.skill_recommendation import (
    SkillRecommendation,
)


class LearningPath(BaseModel):

    model_config = ConfigDict(
        frozen=True,
    )

    steps: list[SkillRecommendation] = Field(
        default_factory=list,
    )