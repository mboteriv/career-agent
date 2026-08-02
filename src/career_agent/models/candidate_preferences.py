from pydantic import BaseModel, ConfigDict


class CandidatePreferences(BaseModel):

    model_config = ConfigDict(frozen=True)

    willing_to_relocate: bool = False

    willing_to_travel: bool = False