from career_agent.models.language_levels import (
    LANGUAGE_LEVELS,
)
from career_agent.services.job_matching_service import (
    JobMatchingService,
)


def test_higher_language_level_matches():

    service = JobMatchingService()

    assert service._language_level_matches(
        "C1",
        "B2",
    )
    
def test_same_language_level_matches():

    service = JobMatchingService()

    assert service._language_level_matches(
        "B2",
        "B2",
    )
    
def test_lower_language_level_does_not_match():

    service = JobMatchingService()

    assert not service._language_level_matches(
        "B1",
        "B2",
    )
    
def test_unknown_language_level_does_not_match():

    service = JobMatchingService()

    assert not service._language_level_matches(
        "Native",
        "B2",
    )