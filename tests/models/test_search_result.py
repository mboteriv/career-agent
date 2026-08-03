from career_agent.models.search_result import SearchResult
from tests.factories import create_job_offer


def test_create_search_result():

    result = SearchResult(
        jobs=[create_job_offer()],
        total=1,
        page=1,
        page_size=20,
    )

    assert result.total == 1
    assert len(result.jobs) == 1
    assert result.page == 1
    assert result.page_size == 20