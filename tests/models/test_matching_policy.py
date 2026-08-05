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
    
def test_required_criteria_is_empty_by_default():

    policy = MatchingPolicy()

    assert policy.required_criteria == frozenset()
    
def test_required_criteria_can_be_configured():

    policy = MatchingPolicy(
        required_criteria=frozenset({
            MatchingCriterion.SKILLS,
            MatchingCriterion.LANGUAGES,
        }),
    )

    assert policy.required_criteria == frozenset({
        MatchingCriterion.SKILLS,
        MatchingCriterion.LANGUAGES,
    })