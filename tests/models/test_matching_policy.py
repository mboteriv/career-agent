from career_agent.models.matching_policy import (
    MatchingPolicy,
)


def test_create_matching_policy():

    policy = MatchingPolicy()

    assert policy.skills_weight == 4.0
    assert policy.experience_weight == 3.0
    assert policy.languages_weight == 2.0
    assert policy.salary_weight == 1.0
    assert policy.remote_weight == 1.0