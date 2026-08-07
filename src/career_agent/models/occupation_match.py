from pydantic import BaseModel, ConfigDict
from career_agent.models.semantic_entity import SemanticEntity

from career_agent.models.skill_gap import SkillGap


class OccupationMatch(BaseModel):

    model_config = ConfigDict(
        frozen=True,
    )

    occupation: SemanticEntity
    
    score: float

    skill_gap: SkillGap