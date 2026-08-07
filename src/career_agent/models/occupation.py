from pydantic import BaseModel, ConfigDict, Field


class Occupation(BaseModel):

    model_config = ConfigDict(
        frozen=True,
    )

    id: str

    preferred_label: str

    description: str | None = None

    aliases: list[str] = Field(
        default_factory=list,
    )