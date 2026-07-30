from career_agent.collectors.greenhouse_collector import GreenhouseCollector

from career_agent.services.job_import_service import JobImportService

service = JobImportService()

jobs = service.import_jobs("canonical")

print(f"{len(jobs)} jobs")

for job in jobs[:5]:
    print(job.title)

