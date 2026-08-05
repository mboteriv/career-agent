from career_agent.models.criterion_match import (
    CriterionMatch,
)
from career_agent.models.matching_criterion import (
    MatchingCriterion,
)
import pytest

def test_create_criterion_match():

    result = CriterionMatch(
        criterion=MatchingCriterion.SKILLS,
        score=1.0,
    )

    assert result.criterion == MatchingCriterion.SKILLS
    assert result.score == 1.0
    
def test_criterion_match_is_immutable():

    result = CriterionMatch(
        criterion=MatchingCriterion.SKILLS,
        score=1.0,
    )

    with pytest.raises(Exception):
        result.score = 0.5
        
def test_create_criterion_match_with_explanation():

    result = CriterionMatch(
        criterion=MatchingCriterion.SKILLS,
        score=1.0,
        explanation="Python",
    )

    assert result.explanation == "Python"
    
def test_create_criterion_match_without_explanation():

    result = CriterionMatch(
        criterion=MatchingCriterion.SKILLS,
        score=1.0,
    )

    assert result.explanation is None
    
def test_create_criterion_match_with_matched_requirements():

    result = CriterionMatch(
        criterion=MatchingCriterion.SKILLS,
        score=1.0,
        matched=[
            "Python",
            "Docker",
        ],
    )

    assert result.matched == [
        "Python",
        "Docker",
    ]
    
def test_create_criterion_match_with_missing_requirements():

    result = CriterionMatch(
        criterion=MatchingCriterion.SKILLS,
        score=0.5,
        missing=[
            "Kubernetes",
        ],
    )

    assert result.missing == [
        "Kubernetes",
    ]
    
def test_create_criterion_match_with_empty_requirements():

    result = CriterionMatch(
        criterion=MatchingCriterion.SKILLS,
        score=1.0,
    )

    assert result.matched == []
    assert result.missing == []
    
def test_create_criterion_match_is_applicable_by_default():

    result = CriterionMatch(
        criterion=MatchingCriterion.SKILLS,
        score=1.0,
    )

    assert result.applicable is True
    
def test_create_criterion_match_with_non_applicable():

    result = CriterionMatch(
        criterion=MatchingCriterion.SKILLS,
        score=0.0,
        applicable=False,
    )

    assert result.applicable is False
    
