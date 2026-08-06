import pytest
from pydantic import ValidationError

from career_agent.models.candidate_preferences import (
    CandidatePreferences,
)
from career_agent.models.enums import RemoteType
from career_agent.models.salary_expectation import (
    SalaryExpectation,
)


def test_create_candidate_preferences():

    preferences = CandidatePreferences(
        willing_to_relocate=True,
        willing_to_travel=False,
    )

    assert preferences.willing_to_relocate is True
    assert preferences.willing_to_travel is False


def test_candidate_preferences_is_immutable():

    preferences = CandidatePreferences()

    with pytest.raises(ValidationError):
        preferences.willing_to_relocate = True
        
def test_create_empty_candidate_preferences():

    preferences = CandidatePreferences()

    assert preferences.preferred_remote_type is None
    assert preferences.preferred_countries == []
    assert preferences.salary_expectation is None
    
def test_create_candidate_preferences():

    preferences = CandidatePreferences(
        preferred_remote_type=RemoteType.REMOTE,
        preferred_countries=[
            "Spain",
            "Germany",
        ],
        salary_expectation=SalaryExpectation(
            amount=50000,
            currency="EUR",
        ),
    )

    assert preferences.preferred_remote_type == (
        RemoteType.REMOTE
    )

    assert preferences.preferred_countries == [
        "Spain",
        "Germany",
    ]
    
    assert (
        preferences.salary_expectation.amount
        == 50000
    )

    assert (
        preferences.salary_expectation.currency
        == "EUR"
    )