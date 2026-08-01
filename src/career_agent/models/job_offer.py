from datetime import datetime

from pydantic import BaseModel, ConfigDict

from career_agent.models.enums import (
    EmploymentType,
    RemoteType,
    Source,
)


class JobOffer(BaseModel):
    """Normalized job offer within the Career Agent domain."""

    model_config = ConfigDict(frozen=True)

    # Identity

    id: str
    source: Source
    url: str

    # Business data

    title: str
    company_name: str
    description: str
    location: str
    employment_type: EmploymentType
    remote_type: RemoteType

    # Metadata

    created_at: datetime
