from typer.testing import CliRunner

from career_agent.cli import app
from career_agent.models.match_result import MatchResult
from career_agent.models.recommendation_options import (
    RecommendationOptions,
)
from tests.factories import create_job_offer



runner = CliRunner()


class FakeWorkflow:

    def execute(
        self,
        options,
    ):

        return [
            MatchResult(
                job=create_job_offer(
                    title="Backend Engineer",
                ),
                score=1.0,
                matched_requirements=[
                    "Python",
                    "Docker",
                ],
                missing_requirements=[
                    "Kubernetes",
                ],
            ),
        ]


def test_recommend_command_shows_job_titles(
    monkeypatch,
):

    monkeypatch.setattr(
        "career_agent.cli._recommendation_workflow",
        lambda: FakeWorkflow(),
    )

    result = runner.invoke(
        app,
        [
            "recommend",
        ],
    )

    assert result.exit_code == 0

    assert "Backend Engineer" in result.stdout
    assert "100%" in result.stdout

    assert "Matched:" in result.stdout
    assert "Python" in result.stdout
    assert "Docker" in result.stdout

    assert "Missing:" in result.stdout
    assert "Kubernetes" in result.stdout
    
    assert "Example Inc." in result.stdout
    assert "Málaga, Spain" in result.stdout
    
    assert "https://example.com/job/123" in result.stdout
    
def test_recommend_command_accepts_limit_option(
    monkeypatch,
):

    captured_options = None

    class FakeWorkflow:

        def execute(
            self,
            options,
        ):
            nonlocal captured_options

            captured_options = options

            return []

    monkeypatch.setattr(
        "career_agent.cli._recommendation_workflow",
        lambda: FakeWorkflow(),
    )

    result = runner.invoke(
        app,
        [
            "recommend",
            "--limit",
            "5",
        ],
    )

    assert result.exit_code == 0

    assert captured_options.limit == 5
    
def test_recommend_command_accepts_min_score_option(
    monkeypatch,
):

    captured_options = None

    class FakeWorkflow:

        def execute(
            self,
            options,
        ):
            nonlocal captured_options

            captured_options = options

            return []

    monkeypatch.setattr(
        "career_agent.cli._recommendation_workflow",
        lambda: FakeWorkflow(),
    )

    result = runner.invoke(
        app,
        [
            "recommend",
            "--min-score",
            "0.75",
        ],
    )

    assert result.exit_code == 0

    assert captured_options.min_score == 0.75