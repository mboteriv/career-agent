from datetime import datetime

from career_agent.models.enums import Source
from career_agent.models.enums import (
    EmploymentType,
    RemoteType,
    Source,
)
from career_agent.models.job_offer import JobOffer

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