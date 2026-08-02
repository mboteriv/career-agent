from datetime import datetime

from pydantic import BaseModel, ConfigDict

from career_agent.models.enums import (
    EmploymentType,
    RemoteType,
    Source,
)
from career_agent.models.salary_expectation import (
    SalaryExpectation,
)
from career_agent.models.job_requirements import JobRequirements

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
    salary: SalaryExpectation | None = None
    requirements: JobRequirements = JobRequirements()

    # Metadata

    created_at: datetime
