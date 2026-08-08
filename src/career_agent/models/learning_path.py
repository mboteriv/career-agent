from pydantic import BaseModel, ConfigDict, Field

from career_agent.models.skill_recommendation import (
    SkillRecommendation,
)
from career_agent.models.skill_dependency import SkillDependency


class LearningPath(BaseModel):

    model_config = ConfigDict(
        frozen=True,
    )

    steps: list[SkillRecommendation] = Field(
        default_factory=list,
    )
    
    dependencies: list[SkillDependency] = Field(
        default_factory=list,
    )