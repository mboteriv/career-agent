from pydantic import BaseModel, ConfigDict, Field

from career_agent.models.job_offer import JobOffer
from pydantic import Field


class MatchResult(BaseModel):

    model_config = ConfigDict(frozen=True)
    
    job: JobOffer

    score: float
    
    matched_requirements: list[str] = Field(default_factory=list)
    missing_requirements: list[str] = Field(default_factory=list)