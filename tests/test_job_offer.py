from datetime import datetime

import pytest
from pydantic import ValidationError

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


def test_create_job_offer():
    job = create_job_offer()

    assert job.title == "Backend Engineer"
    assert job.source == Source.GREENHOUSE


def test_job_offer_is_immutable():
    job = create_job_offer()

    with pytest.raises(Exception):
        job.title = "Frontend Engineer"


def test_job_offer_supports_employment_type():
    job = create_job_offer(
        employment_type=EmploymentType.CONTRACT
    )

    assert job.employment_type == EmploymentType.CONTRACT


def test_job_offer_supports_remote_type():
    job = create_job_offer(
        remote_type=RemoteType.HYBRID
    )

    assert job.remote_type == RemoteType.HYBRID


def test_invalid_remote_type_raises_validation_error():
    with pytest.raises(ValidationError):
        create_job_offer(
            remote_type="teletransportado"
        )