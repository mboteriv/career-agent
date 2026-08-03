from career_agent.models.recommendation_options import (
    RecommendationOptions,
)
import pytest

from pydantic import ValidationError


def test_recommendation_options_is_immutable():

    options = RecommendationOptions()

    with pytest.raises(
        ValidationError,
    ):
        options.limit = 10


def test_create_recommendation_options():

    options = RecommendationOptions()

    assert options.limit is None
    assert options.min_score is None