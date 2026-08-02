import pytest
from pydantic import ValidationError

from career_agent.models.candidate_preferences import (
    CandidatePreferences,
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