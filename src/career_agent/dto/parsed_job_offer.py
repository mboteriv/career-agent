from datetime import datetime

from pydantic import BaseModel, ConfigDict

from career_agent.models.enums import Source


class ParsedJobOffer(BaseModel):
    model_config = ConfigDict(frozen=True)

    source: Source
    collected_at: datetime
    id: str

    title: str
    company_name: str
    description: str

    location: str

    employment_type: str
    remote_type: str

    source_url: str

