from career_agent.models.enums import Source
from career_agent.models.parsed_job_offer import ParsedJobOffer
from career_agent.models.source_job_offer import SourceJobOffer


class LeverParser:

    def parse(
        self,
        source_offer: SourceJobOffer,
    ) -> ParsedJobOffer:

        payload = source_offer.raw_data

        categories = payload.get("categories", {})

        return ParsedJobOffer(
            id=payload["id"],
            source=source_offer.source,
            url=payload["hostedUrl"],
            title=payload["text"],
            company_name=source_offer.metadata.get("company_name", ""),
            description=payload["description"],
            location=categories.get("location", ""),
            employment_type=categories.get("commitment", ""),
        )