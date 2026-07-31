from career_agent.providers.greenhouse_provider import greenhouse_provider
from career_agent.services.job_import_service import JobImportService
from career_agent.services.job_import_service import JobImportService
from career_agent.providers.ats_provider import ATSProvider

service = JobImportService(
    provider=greenhouse_provider(),
)

jobs = service.import_jobs("canonical")

print(f"{len(jobs)} jobs")

for job in jobs[:5]:
    print(job.title)

