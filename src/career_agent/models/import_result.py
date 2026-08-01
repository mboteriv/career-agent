from pydantic import BaseModel, ConfigDict


from career_agent.models.job_offer import JobOffer


class ImportResult(BaseModel):

    model_config = ConfigDict(frozen=True)

    new_jobs: list[JobOffer]

    updated_jobs: list[JobOffer]

    unchanged_jobs: list[JobOffer]

    removed_jobs: list[JobOffer]

    