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

    total_essential: int = 0

    total_optional: int = 0

    @property
    def essential_coverage(
        self,
    ) -> float:

        if self.total_essential == 0:
            return 1.0

        return (
            self.total_essential
            - len(self.missing_essential)
        ) / self.total_essential

    @property
    def optional_coverage(
        self,
    ) -> float:

        if self.total_optional == 0:
            return 1.0

        return (
            self.total_optional
            - len(self.missing_optional)
        ) / self.total_optional