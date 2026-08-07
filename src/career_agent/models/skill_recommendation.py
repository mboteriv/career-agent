from pydantic import BaseModel, ConfigDict

from career_agent.models.semantic_entity import SemanticEntity
from career_agent.models.recommendation_priority import (
    RecommendationPriority,
)

class SkillRecommendation(BaseModel):

    model_config = ConfigDict(
        frozen=True,
    )

    skill: SemanticEntity

    priority: RecommendationPriority