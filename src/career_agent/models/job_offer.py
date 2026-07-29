from datetime import datetime

from pydantic import BaseModel, ConfigDict

from career_agent.models.enums import Source

import pytest

from career_agent.models.enums import (
    EmploymentType,
    RemoteType,
    Source,
)

def test_job_offer_is_immutable():
    job = JobOffer(
        id="123",
        source=Source.GREENHOUSE,
        url="https://example.com/job/123",
        title="Backend Engineer",
        company="Example Inc.",
        description="Example description",
        created_at=datetime.now(),
    )

    with pytest.raises(Exception):
        job.title = "Frontend Engineer"

def create_job_offer(**kwargs) -> JobOffer:
    data = {
        "id": "123",
        "source": Source.GREENHOUSE,
        "url": "https://example.com/job/123",
        "title": "Backend Engineer",
        "company_name": "Example Inc.",
        "description": "Example description",
        "location": "Málaga, Spain",
        "employment_type": EmploymentType.FULL_TIME,
        "remote_type": RemoteType.REMOTE,
        "created_at": datetime.now(),
    }

    data.update(kwargs)
    return JobOffer(**data)

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
