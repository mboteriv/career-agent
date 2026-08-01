from career_agent.dto.parsed_job_offer import ParsedJobOffer


class GreenhouseParser:

    def parse(self, source):
        payload = source.payload

        return ParsedJobOffer(
            id=str(payload["id"]),
            source=source.source,
            collected_at=source.collected_at,

            title=payload.get("title", ""),
            company_name=payload.get("company_name", ""),
            description=payload.get("content", ""),
            location=payload.get("location", {}).get("name", ""),

            employment_type="",
            remote_type="",

            source_url=payload.get("absolute_url", ""),
        )