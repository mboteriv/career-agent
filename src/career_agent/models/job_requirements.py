from pydantic import BaseModel, ConfigDict

from career_agent.models.language_skill import LanguageSkill


class JobRequirements(BaseModel):

    model_config = ConfigDict(frozen=True)

    skills: list[str] = []

    languages: list[LanguageSkill] = []

    years_experience: int | None = None