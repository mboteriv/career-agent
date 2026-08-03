from pydantic import BaseModel, ConfigDict


class RecommendationOptions(BaseModel):

    model_config = ConfigDict(
        frozen=True,
    )

    limit: int | None = None

    min_score: float | None = None