from career_agent.collectors.greenhouse_collector import GreenhouseCollector
from career_agent.parsers.greenhouse_parser import GreenhouseParser
from career_agent.services.job_import_service import JobImportService

service = JobImportService(
    collector=GreenhouseCollector(),
    parser=GreenhouseParser(),
)

jobs = service.import_jobs("canonical")

print(f"{len(jobs)} jobs")

for job in jobs[:5]:
    print(job.title)

