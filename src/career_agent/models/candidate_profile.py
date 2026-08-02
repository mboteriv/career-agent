from pydantic import BaseModel, ConfigDict

from career_agent.models.language_skill import LanguageSkill
from career_agent.models.salary_expectation import SalaryExpectation
from career_agent.models.enums import RemoteType
from career_agent.models.candidate_preferences import (
    CandidatePreferences,
)


class CandidateProfile(BaseModel):

    model_config = ConfigDict(frozen=True)
    skills: list[str] = []
    languages: list[LanguageSkill] = []
    years_experience: int = 0
    salary: SalaryExpectation | None = None
    preferred_remote_type: RemoteType | None = None
    preferred_countries: list[str] = []
    preferences: CandidatePreferences = CandidatePreferences()
    skills: list[str] = []
    
