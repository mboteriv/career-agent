from enum import StrEnum
from pydantic import BaseModel
from pydantic import ConfigDict


class MatchingCriterion(StrEnum):

    REMOTE = "remote"
    COUNTRY = "country"
    SALARY = "salary"
    SKILLS = "skills"
    LANGUAGES = "languages"
    EXPERIENCE = "experience"
    