from career_agent.collectors.greenhouse_collector import GreenhouseCollector
from career_agent.parsers.greenhouse_parser import GreenhouseParser
from career_agent.services.job_import_service import JobImportService


def test_import_jobs():
    service = JobImportService(
        collector=GreenhouseCollector(),
        parser=GreenhouseParser(),
    )

    jobs = service.import_jobs("canonical")

    assert len(jobs) > 0