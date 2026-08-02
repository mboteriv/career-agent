from pydantic import BaseModel, ConfigDict


class MatchResult(BaseModel):

    model_config = ConfigDict(frozen=True)

    score: float