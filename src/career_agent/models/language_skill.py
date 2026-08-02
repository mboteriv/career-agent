from pydantic import BaseModel, ConfigDict


class LanguageSkill(BaseModel):

    model_config = ConfigDict(frozen=True)

    language: str
    level: str