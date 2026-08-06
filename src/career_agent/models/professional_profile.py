from pydantic import BaseModel, ConfigDict, Field


class ProfessionalProfile(BaseModel):

    model_config = ConfigDict(
        frozen=True,
    )

    occupations: list[str] = Field(
        default_factory=list,
    )

    capabilities: list[str] = Field(
        default_factory=list,
    )

    skills: list[str] = Field(
        default_factory=list,
    )

    knowledge: list[str] = Field(
        default_factory=list,
    )

    languages: list[str] = Field(
        default_factory=list,
    )