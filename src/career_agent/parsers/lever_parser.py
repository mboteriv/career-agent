from career_agent.models.enums import Source
from career_agent.models.parsed_job_offer import ParsedJobOffer
from career_agent.models.source_job_offer import SourceJobOffer


class LeverParser:

    def parse(
        self,
        source_offer: SourceJobOffer,
    ) -> ParsedJobOffer:

        payload = source_offer.raw_data

        return ParsedJobOffer(
            id=payload["id"],
            source=source_offer.source,
            url=payload["hostedUrl"],
            title=payload["text"],
            company_name="",
            description=payload["description"],
            location=payload["categories"]["location"],
            employment_type=payload["categories"]["commitment"],
        )