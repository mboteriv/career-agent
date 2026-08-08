from pydantic import BaseModel, ConfigDict, Field


class LearningPathExplanation(BaseModel):

    model_config = ConfigDict(
        frozen=True,
    )

    summary: str

    reasons: list[str] = Field(
        default_factory=list,
    )