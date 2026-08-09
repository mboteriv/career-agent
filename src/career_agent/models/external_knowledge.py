from pydantic import BaseModel, ConfigDict, Field

from career_agent.models.semantic_entity import (
    SemanticEntity,
)
from career_agent.models.occupation_skill_relation import (
    OccupationSkillRelation,
)


class ExternalKnowledge(BaseModel):

    model_config = ConfigDict(
        frozen=True,
    )

    skills: list[SemanticEntity] = Field(
        default_factory=list,
    )

    occupations: list[SemanticEntity] = Field(
        default_factory=list,
    )
    
    occupation_skill_relations: list[
        OccupationSkillRelation
    ] = Field(
        default_factory=list,
    )
    
