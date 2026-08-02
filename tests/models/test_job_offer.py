from datetime import datetime

import pytest
from pydantic import ValidationError

from career_agent.models.enums import (
    EmploymentType,
    RemoteType,
    Source,
)
from career_agent.models.job_offer import JobOffer
from career_agent.testing.factories import create_job_offer
from career_agent.models.salary_expectation import (
    SalaryExpectation,
)
from career_agent.models.job_requirements import JobRequirements


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
    with pytest.raises(Exception):
        create_job_offer(
            remote_type="teletransportado"
        )
        
def test_job_offer_supports_salary():

    offer = create_job_offer(
        salary=SalaryExpectation(
            amount=70000,
        ),
    )

    assert offer.salary.amount == 70000
    assert offer.salary.currency == "EUR"
    
def test_job_offer_supports_requirements():

    offer = create_job_offer(
        requirements=JobRequirements(
            skills=[
                "Python",
            ],
        ),
    )

    assert offer.requirements.skills == [
        "Python",
    ]