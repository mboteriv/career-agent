from pydantic import BaseModel, ConfigDict, Field


class CVExtraction(BaseModel):

    model_config = ConfigDict(
        frozen=True,
    )

    summary: str = ""

    experience: list[str] = Field(
        default_factory=list,
    )

    education: list[str] = Field(
        default_factory=list,
    )

    skills: list[str] = Field(
        default_factory=list,
    )

    languages: list[str] = Field(
        default_factory=list,
    )