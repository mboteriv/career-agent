from pydantic import BaseModel, ConfigDict, Field


class RecommendationExplanation(BaseModel):

    model_config = ConfigDict(
        frozen=True,
    )

    summary: str

    reasons: list[str] = Field(
        default_factory=list,
    )