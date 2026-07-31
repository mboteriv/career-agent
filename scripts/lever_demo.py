from career_agent.collectors.lever_collector import LeverCollector
from career_agent.parsers.lever_parser import LeverParser
from career_agent.services.job_import_service import JobImportService

service = JobImportService(
    collector=LeverCollector(),
    parser=LeverParser(),
)

jobs = service.import_jobs("canonical")

print(f"{len(jobs)} jobs")

for job in jobs[:5]:
    print(job.title)