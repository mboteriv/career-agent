from pydantic import BaseModel, ConfigDict, Field


class SemanticEntity(BaseModel):

    model_config = ConfigDict(
        frozen=True,
    )

    id: str

    preferred_label: str

    aliases: list[str] = Field(
        default_factory=list,
    )

    external_ids: dict[str, str] = Field(
        default_factory=dict,
    )