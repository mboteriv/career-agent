from career_agent.models.matching_criterion import MatchingCriterion
from career_agent.models.matching_policy import MatchingPolicy


def test_returns_skills_weight():

    policy = MatchingPolicy()

    assert (
        policy.weight_for(
            MatchingCriterion.SKILLS,
        )
        == 4.0
    )
    
def test_returns_experience_weight():

    policy = MatchingPolicy()

    assert (
        policy.weight_for(
            MatchingCriterion.EXPERIENCE,
        )
        == 3.0
    )
    
def test_returns_languages_weight():

    policy = MatchingPolicy()

    assert (
        policy.weight_for(
            MatchingCriterion.LANGUAGES,
        )
        == 2.0
    )

def test_returns_default_weights():

    policy = MatchingPolicy()

    assert (
        policy.weight_for(
            MatchingCriterion.SALARY,
        )
        == 1.0
    )

    assert (
        policy.weight_for(
            MatchingCriterion.REMOTE,
        )
        == 1.0
    )

    assert (
        policy.weight_for(
            MatchingCriterion.COUNTRY,
        )
        == 1.0
    )