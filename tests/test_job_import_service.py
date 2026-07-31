from career_agent.collectors.greenhouse_collector import GreenhouseCollector
from career_agent.parsers.greenhouse_parser import GreenhouseParser
from career_agent.services.job_import_service import JobImportService
from career_agent.providers.greenhouse_provider import greenhouse_provider

def test_import_jobs():
    service = JobImportService(
        provider=greenhouse_provider(),
    )

    jobs = service.import_jobs("canonical")

    assert len(jobs) > 0