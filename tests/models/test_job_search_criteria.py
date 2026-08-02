from career_agent.models.job_search_criteria import (
    JobSearchCriteria,
)
from sqlmodel import select
from career_agent.models.job_sort_field import JobSortField
from datetime import datetime


def test_create_job_search_criteria():

    criteria = JobSearchCriteria()

    assert criteria.keywords == []
    assert criteria.company_name is None
    assert criteria.location is None
    assert criteria.employment_type is None
    assert criteria.remote_type is None

from career_agent.models.enums import (
    EmploymentType,
    RemoteType,
)


def test_job_search_criteria_supports_filters():

    criteria = JobSearchCriteria(
        keywords=["python", "backend"],
        company_name="Canonical",
        location="Spain",
        employment_type=EmploymentType.FULL_TIME,
        remote_type=RemoteType.REMOTE,
    )

    assert criteria.keywords == ["python", "backend"]
    assert criteria.company_name == "Canonical"
    assert criteria.location == "Spain"
    assert criteria.employment_type is EmploymentType.FULL_TIME
    assert criteria.remote_type is RemoteType.REMOTE

import pytest


def test_job_search_criteria_is_immutable():

    criteria = JobSearchCriteria()

    with pytest.raises(Exception):
        criteria.company_name = "Canonical"

def search(
    self,
    criteria: JobSearchCriteria,
) -> list[JobOffer]:
    with get_session() as session:

        statement = select(JobOfferRecord)

        if criteria.company_name:
            statement = statement.where(
                JobOfferRecord.company_name
                == criteria.company_name
            )

        records = session.exec(statement).all()

        return [
            self._to_domain(record)
            for record in records
        ]

def test_job_search_criteria_supports_sorting():

    criteria = JobSearchCriteria(
        sort_by=JobSortField.CREATED_AT,
    )

    assert criteria.sort_by is JobSortField.CREATED_AT
    assert criteria.descending is True

def test_job_search_criteria_supports_created_after():

    date = datetime(2026, 1, 15)

    criteria = JobSearchCriteria(
        created_after=date,
    )

    assert criteria.created_after == date

def test_job_search_criteria_supports_created_before():

    date = datetime(2026, 2, 1)

    criteria = JobSearchCriteria(
        created_before=date,
    )

    assert criteria.created_before == date