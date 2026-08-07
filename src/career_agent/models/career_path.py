from pydantic import BaseModel, ConfigDict, Field

from career_agent.models.occupation_match import (
    OccupationMatch,
)


class CareerPath(BaseModel):

    model_config = ConfigDict(
        frozen=True,
    )

    occupations: list[OccupationMatch] = Field(
        default_factory=list,
    )