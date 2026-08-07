from pydantic import BaseModel, ConfigDict


class OccupationSkillRelation(BaseModel):

    model_config = ConfigDict(
        frozen=True,
    )

    occupation_id: str

    skill_id: str

    relation_type: str