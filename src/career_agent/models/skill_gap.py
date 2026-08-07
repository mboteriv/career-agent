from pydantic import BaseModel, ConfigDict, Field

from career_agent.models.semantic_entity import SemanticEntity


class SkillGap(BaseModel):

    model_config = ConfigDict(
        frozen=True,
    )

    missing_essential: list[SemanticEntity] = Field(
        default_factory=list,
    )

    missing_optional: list[SemanticEntity] = Field(
        default_factory=list,
    )