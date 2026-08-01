from career_agent.models.import_result import ImportResult
from career_agent.normalizers.job_offer_normalizer import JobOfferNormalizer
from career_agent.models.job_offer import JobOffer
from career_agent.providers.ats_provider import ATSProvider
from career_agent.repositories.job_offer_repository import (
    JobOfferRepository,
)
from career_agent.models.import_result import ImportResult

class JobImportService:

    def __init__(
        self,
        provider: ATSProvider,
        repository=None,
        normalizer=None,
    ) -> None:

        self._collector = provider.collector
        self._parser = provider.parser
        self._normalizer = (
            normalizer
            or JobOfferNormalizer()
        )
        self._repository = (
            repository
            or JobOfferRepository()
        )
    def import_jobs(
        self,
        board: str,
    ) -> list[JobOffer]:

        source_offers = self._collector.collect_from_api(board)

        jobs = [
            self._normalizer.normalize(
            self._parser.parse(source_offer)
            )
            for source_offer in source_offers
        ]

        new_jobs = []
        updated_jobs = []
        unchanged_jobs = []

        for job in jobs:
            self._classify_job(
                job,
                new_jobs,
                updated_jobs,
                unchanged_jobs,
            )

        return ImportResult(
            new_jobs=new_jobs,
            updated_jobs=updated_jobs,
            unchanged_jobs=unchanged_jobs,
            removed_jobs=[],
        )

    def _classify_job(
        self,
        job: JobOffer,
        new_jobs: list[JobOffer],
        updated_jobs: list[JobOffer],
        unchanged_jobs: list[JobOffer],
    ) -> None:

        existing = self._repository.get_by_id(
            job.source,
            job.id,
        )

        if existing is None:
            self._repository.save(job)
            new_jobs.append(job)

        elif self._has_changed(existing, job):
            self._repository.update(job)
            updated_jobs.append(job)

        else:
            unchanged_jobs.append(job)

    def _has_changed(
        self,
        existing: JobOffer,
        incoming: JobOffer,
    ) -> bool:

        return (
            existing.title != incoming.title
            or existing.description != incoming.description
            or existing.location != incoming.location
            or existing.employment_type != incoming.employment_type
            or existing.remote_type != incoming.remote_type
        )