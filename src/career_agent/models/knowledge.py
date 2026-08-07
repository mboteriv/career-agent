from pydantic import BaseModel, ConfigDict, Field

from career_agent.models.external_knowledge import ExternalKnowledge
from career_agent.models.semantic_entity import (
    SemanticEntity,
)
from career_agent.models.occupation_skill_relation import (
    OccupationSkillRelation,
)
from career_agent.models.skill_dependency import (
    SkillDependency,
)

class Knowledge(BaseModel):

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
    
    skill_dependencies: list[SkillDependency] = Field(
        default_factory=list,
    )
    
class KnowledgeCompiler:

    def compile(
        self,
        external: ExternalKnowledge,
    ) -> Knowledge:

        return Knowledge(
            skills=external.skills,
            occupations=external.occupations,
        )