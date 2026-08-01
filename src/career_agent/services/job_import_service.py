from career_agent.normalizers.job_offer_normalizer import JobOfferNormalizer
from career_agent.models.job_offer import JobOffer
from career_agent.providers.ats_provider import ATSProvider
from career_agent.repositories.job_offer_repository import (
    JobOfferRepository,
)

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

        self._repository.save_all(jobs)

        return jobs