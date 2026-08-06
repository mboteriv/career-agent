from pydantic import BaseModel, ConfigDict, Field

from career_agent.models.enums import RemoteType
from career_agent.models.salary_expectation import (
    SalaryExpectation,
)

class CandidatePreferences(BaseModel):

    model_config = ConfigDict(frozen=True)

    willing_to_relocate: bool = False

    willing_to_travel: bool = False
    
    preferred_remote_type: RemoteType | None = None

    preferred_countries: list[str] = Field(
        default_factory=list,
    )

    salary_expectation: SalaryExpectation | None = None