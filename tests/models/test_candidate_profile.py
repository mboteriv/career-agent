import pytest
from pydantic import ValidationError

from career_agent.models.candidate_profile import (
    CandidateProfile,
)
from career_agent.models.professional_profile import (
    ProfessionalProfile,
)
from career_agent.models.language_skill import LanguageSkill
from career_agent.models.salary_expectation import SalaryExpectation
from career_agent.models.enums import RemoteType
from career_agent.models.candidate_preferences import (
    CandidatePreferences,
)


def test_candidate_profile_is_immutable():

    profile = CandidateProfile()

    with pytest.raises(ValidationError):
        profile.skills = []
        
def test_candidate_profile_supports_skills():

    profile = CandidateProfile(
        skills=[
            "Python",
            "Docker",
            "SQL",
        ],
    )

    assert profile.skills == [
        "Python",
        "Docker",
        "SQL",
    ]

def test_candidate_profile_supports_languages():

    profile = CandidateProfile(
        languages=[
            LanguageSkill(
                language="English",
                level="C1",
            ),
        ],
    )

    assert profile.languages[0].language == "English"
    
def test_candidate_profile_supports_experience():

    profile = CandidateProfile(
        years_experience=5,
    )

    assert profile.years_experience == 5
    
def test_candidate_profile_supports_salary():

    profile = CandidateProfile(
        salary=SalaryExpectation(
            amount=60000,
        ),
    )

    assert profile.salary.amount == 60000
    assert profile.salary.currency == "EUR"
    
def test_candidate_profile_supports_preferred_remote_type():

    profile = CandidateProfile(
        preferred_remote_type=RemoteType.REMOTE,
    )

    assert (
        profile.preferred_remote_type
        == RemoteType.REMOTE
    )
    
def test_candidate_profile_supports_preferred_countries():

    profile = CandidateProfile(
        preferred_countries=[
            "Spain",
            "Portugal",
            "Germany",
        ],
    )

    assert profile.preferred_countries == [
        "Spain",
        "Portugal",
        "Germany",
    ]
    
def test_candidate_profile_supports_preferences():

    profile = CandidateProfile(
        preferences=CandidatePreferences(
            willing_to_relocate=True,
        ),
    )

    assert profile.preferences.willing_to_relocate is True
    assert profile.preferences.willing_to_travel is False
    
def test_candidate_profile_supports_skills():

    profile = CandidateProfile(
        skills=[
            "Python",
            "Docker",
        ],
    )

    assert profile.skills == [
        "Python",
        "Docker",
    ]
    
def test_create_candidate_profile_contains_professional_profile():

    profile = CandidateProfile()

    assert isinstance(
        profile.professional_profile,
        ProfessionalProfile,
    )
    
def test_create_candidate_profile_contains_preferences():

    profile = CandidateProfile()

    assert isinstance(
        profile.preferences,
        CandidatePreferences,
    )