from career_agent.normalizers.job_offer_normalizer import JobOfferNormalizer
from career_agent.models.job_offer import JobOffer


class JobImportService:

    def __init__(
        self,
        collector,
        parser,
        normalizer=None,
    ) -> None:

        self._collector = collector
        self._parser = parser
        self._normalizer = (
            normalizer
            or JobOfferNormalizer()
        )

    def import_jobs(
        self,
        board: str,
    ) -> list[JobOffer]:

        source_offers = self._collector.collect_from_api(board)

        return [
            self._normalizer.normalize(
                self._parser.parse(source_offer)
            )
            for source_offer in source_offers
        ]