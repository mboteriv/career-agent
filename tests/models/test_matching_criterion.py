from career_agent.models.matching_criterion import (
    MatchingCriterion,
)

def test_matching_criterion_contains_all_criteria():

    assert MatchingCriterion.REMOTE == "remote"
    assert MatchingCriterion.COUNTRY == "country"
    assert MatchingCriterion.SALARY == "salary"
    assert MatchingCriterion.SKILLS == "skills"
    assert MatchingCriterion.LANGUAGES == "languages"
    assert MatchingCriterion.EXPERIENCE == "experience"
    
