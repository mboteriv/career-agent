from career_agent.models.match_result import MatchResult
import pytest
from pydantic import ValidationError


def test_create_match_result():

    result = MatchResult(
        score=0.75,
    )

    assert result.score == 0.75
    
def test_match_result_is_immutable():

    result = MatchResult(
        score=0.75,
    )

    with pytest.raises(ValidationError):
        result.score = 1.0