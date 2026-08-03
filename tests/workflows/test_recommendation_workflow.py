from career_agent.models.candidate_profile import (
    CandidateProfile,
)
from career_agent.models.match_result import MatchResult
from career_agent.models.recommendation_options import RecommendationOptions
from tests.factories import create_job_offer
from career_agent.workflows.recommendation_workflow import (
    RecommendationWorkflow,
)


class FakeProfileRepository:

    def load(
        self,
    ) -> CandidateProfile:

        return CandidateProfile()


class FakeJobRepository:

    def search(
        self,
        *_,
    ):

        return [
            create_job_offer(),
        ]


class FakeRecommendationService:

    def __init__(self):

        self.jobs = None
        self.profile = None

    def recommend(
        self,
        jobs,
        profile,
    ):

        self.jobs = jobs
        self.profile = profile

        return [
            "OK",
        ]


def test_workflow_returns_recommendations():

    recommendation_service = (
        FakeRecommendationService()
    )

    workflow = RecommendationWorkflow(
        profile_repository=FakeProfileRepository(),
        job_repository=FakeJobRepository(),
        recommendation_service=recommendation_service,
    )

    results = workflow.execute(
        RecommendationOptions(),
    )

    assert results == [
        "OK",
    ]

    assert len(
        recommendation_service.jobs,
    ) == 1

    assert isinstance(
        recommendation_service.profile,
        CandidateProfile,
    )
    
def test_workflow_returns_empty_list_when_no_jobs_exist():

    class FakeProfileRepository:

        def load(self):
            return CandidateProfile()

    class FakeJobRepository:

        def search(
            self,
            *_,
        ):
            return []

    class FakeRecommendationService:

        def recommend(
            self,
            jobs,
            profile,
        ):

            assert jobs == []

            return []

    workflow = RecommendationWorkflow(
        profile_repository=FakeProfileRepository(),
        job_repository=FakeJobRepository(),
        recommendation_service=FakeRecommendationService(),
    )

    assert workflow.execute(
        RecommendationOptions(),
    ) == []
    
def test_workflow_limits_recommendations():

    class FakeProfileRepository:

        def load(self):
            return CandidateProfile()

    class FakeJobRepository:

        def search(
            self,
            *_,
        ):
            return []

    class FakeRecommendationService:

        def recommend(
            self,
            jobs,
            profile,
        ):
            return [
                "A",
                "B",
                "C",
                "D",
            ]

    workflow = RecommendationWorkflow(
        profile_repository=FakeProfileRepository(),
        job_repository=FakeJobRepository(),
        recommendation_service=FakeRecommendationService(),
    )

    results = workflow.execute(
        RecommendationOptions(
            limit=2,
        ),
    )

    assert results == [
        "A",
        "B",
    ]
    
def test_workflow_filters_recommendations_by_min_score():

    class FakeProfileRepository:

        def load(self):
            return CandidateProfile()

    class FakeJobRepository:

        def search(
            self,
            *_,
        ):
            return []

    class FakeRecommendationService:

        def recommend(
            self,
            jobs,
            profile,
        ):
            return [
                MatchResult(
                    job=create_job_offer(id="1"),
                    score=0.90,
                ),
                MatchResult(
                    job=create_job_offer(id="2"),
                    score=0.70,
                ),
                MatchResult(
                    job=create_job_offer(id="3"),
                    score=0.50,
                ),
            ]

    workflow = RecommendationWorkflow(
        profile_repository=FakeProfileRepository(),
        job_repository=FakeJobRepository(),
        recommendation_service=FakeRecommendationService(),
    )

    results = workflow.execute(
        RecommendationOptions(
            min_score=0.75,
        ),
    )

    assert len(results) == 1
    assert results[0].job.id == "1"