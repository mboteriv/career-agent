from pydantic import BaseModel, ConfigDict


class SkillDependency(BaseModel):

    model_config = ConfigDict(
        frozen=True,
    )

    prerequisite_skill_id: str

    dependent_skill_id: str