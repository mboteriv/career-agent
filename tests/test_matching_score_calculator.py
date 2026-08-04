from career_agent.services.matching_score_calculator import (
    MatchingScoreCalculator,
)


def test_calculate_returns_maximum_score():

    calculator = MatchingScoreCalculator()

    result = calculator.calculate(
        [
            1.0,
            0.5,
            0.0,
        ],
    )

    assert result == 1.0
    
def test_calculate_returns_zero_for_empty_scores():

    calculator = MatchingScoreCalculator()

    assert calculator.calculate([]) == 0.0