from pydantic import BaseModel
from pydantic import ConfigDict


class MatchingPolicy(BaseModel):

    model_config = ConfigDict(
        frozen=True,
    )

    skills_weight: float = 4.0
    experience_weight: float = 3.0
    languages_weight: float = 2.0
    salary_weight: float = 1.0
    remote_weight: float = 1.0
    country_weight: float = 1.0