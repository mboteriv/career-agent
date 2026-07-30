from career_agent.services.job_import_service import JobImportService


def test_import_jobs():
    service = JobImportService()

    jobs = service.import_jobs("canonical")

    assert len(jobs) > 0