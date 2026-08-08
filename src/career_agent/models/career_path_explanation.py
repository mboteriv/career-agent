from pydantic import ConfigDict, Field, BaseModel


class CareerPathExplanation(BaseModel):

    model_config = ConfigDict(
        frozen=True,
    )

    summary: str

    reasons: list[str] = Field(
        default_factory=list,
    )