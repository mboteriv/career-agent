from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field

from career_agent.models.candidate_profile import CandidateProfile
from career_agent.models.job_offer import JobOffer
from career_agent.models.matching_criterion import (
    MatchingCriterion,
)

    
class CriterionMatch(BaseModel):

    model_config = ConfigDict(
        frozen=True,
    )
    explanation: str | None = None
    
    criterion: MatchingCriterion

    score: float

    applicable: bool = True

    matched: list[str] = Field(
        default_factory=list,
    )

    missing: list[str] = Field(
        default_factory=list,
    )
    
    
    