from career_agent.models.matching_policy import MatchingPolicy
from career_agent.models.criterion_match import CriterionMatch
from career_agent.models.matching_criterion import MatchingCriterion
from career_agent.services.matching_score_calculator import MatchingScoreCalculator
from career_agent.models.matching_policy import MatchingPolicy
import pytest



def test_calculate_returns_zero_for_empty_matches():

    calculator = MatchingScoreCalculator()

    result = calculator.calculate(
        [],
        MatchingPolicy(),
    )

    assert result == 0.0
    
def test_calculate_ignores_non_applicable_criteria():

    calculator = MatchingScoreCalculator()

    result = calculator.calculate(
        [
            CriterionMatch(
                criterion=MatchingCriterion.SKILLS,
                score=0.5,
                applicable=True,
            ),
            CriterionMatch(
                criterion=MatchingCriterion.REMOTE,
                score=1.0,
                applicable=False,
            ),
        ],
        MatchingPolicy(),
    )

    assert result == 0.5
    
def test_calculate_returns_zero_when_no_criteria_are_applicable():

    calculator = MatchingScoreCalculator()

    result = calculator.calculate(
        [
            CriterionMatch(
                criterion=MatchingCriterion.SKILLS,
                score=1.0,
                applicable=False,
            ),
        ],
        MatchingPolicy(),
    )

    assert result == 0.0
    
def test_calculate_returns_weighted_average():

    calculator = MatchingScoreCalculator()

    result = calculator.calculate(
        [
            CriterionMatch(
                criterion=MatchingCriterion.SKILLS,
                score=1.0,
                applicable=True,
            ),
            CriterionMatch(
                criterion=MatchingCriterion.EXPERIENCE,
                score=0.5,
                applicable=True,
            ),
        ],
        MatchingPolicy(),
    )

    assert result == pytest.approx(
        0.7857142857142857,
    )
    
def test_calculate_ignores_non_applicable_criteria():

    calculator = MatchingScoreCalculator()

    result = calculator.calculate(
        [
            CriterionMatch(
                criterion=MatchingCriterion.SKILLS,
                score=1.0,
                applicable=True,
            ),
            CriterionMatch(
                criterion=MatchingCriterion.EXPERIENCE,
                score=0.0,
                applicable=False,
            ),
        ],
        MatchingPolicy(),
    )

    assert result == 1.0