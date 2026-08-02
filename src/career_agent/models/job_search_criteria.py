from pydantic import BaseModel, ConfigDict

from career_agent.models.enums import (
    EmploymentType,
    RemoteType,
)

from career_agent.models.job_sort_field import JobSortField

from datetime import datetime

class JobSearchCriteria(BaseModel):

    model_config = ConfigDict(frozen=True)

    keywords: list[str] = []

    company_name: str | None = None

    location: str | None = None

    employment_type: EmploymentType | None = None

    remote_type: RemoteType | None = None

    created_after: datetime | None = None

    created_before: datetime | None = None

    page: int = 1
    page_size: int = 20

    sort_by: JobSortField | None = None

    descending: bool = True