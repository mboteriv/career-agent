from career_agent.models.import_result import ImportResult
from career_agent.testing.factories import create_job_offer
import pytest


def test_create_import_result():

    job = create_job_offer()

    result = ImportResult(
        new_jobs=[job],
        updated_jobs=[],
        unchanged_jobs=[],
        removed_jobs=[],
    )

    assert len(result.new_jobs) == 1

def test_import_result_is_immutable():

    result = ImportResult(
        new_jobs=[],
        updated_jobs=[],
        unchanged_jobs=[],
        removed_jobs=[],
    )

    with pytest.raises(Exception):
        result.new_jobs = []