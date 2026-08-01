from career_agent.dto.parsed_job_offer import ParsedJobOffer
from career_agent.models.enums import EmploymentType, RemoteType
from career_agent.models.job_offer import JobOffer


class JobOfferNormalizer:

    _EMPLOYMENT_TYPE_MAP = {
        "full time": EmploymentType.FULL_TIME,
        "full-time": EmploymentType.FULL_TIME,
        "fulltime": EmploymentType.FULL_TIME,
        "permanent": EmploymentType.FULL_TIME,

        "part time": EmploymentType.PART_TIME,
        "part-time": EmploymentType.PART_TIME,

        "contract": EmploymentType.CONTRACT,

        "intern": EmploymentType.INTERN,
        "internship": EmploymentType.INTERN,

        "temporary": EmploymentType.TEMPORARY,
        "unknown": EmploymentType.OTHER,
    }

    def _normalize_employment_type(
        self,
        value: str,
    ) -> EmploymentType:
        return self._EMPLOYMENT_TYPE_MAP.get(
            value.strip().lower(),
            EmploymentType.OTHER,
        )

    def normalize(
        self,
        parsed: ParsedJobOffer,
    ) -> JobOffer:

        return JobOffer(
            id=parsed.id,
            source=parsed.source,
            url=parsed.source_url,

            title=parsed.title,
            company_name=parsed.company_name,
            description=parsed.description,
            location=parsed.location,

            employment_type=self._normalize_employment_type(
                parsed.employment_type
            ),

            remote_type=self._normalize_remote_type(
                parsed.remote_type
            ),

            created_at=parsed.collected_at,
        )

    _REMOTE_TYPE_MAP = {
        "remote": RemoteType.REMOTE,
        "hybrid": RemoteType.HYBRID,
        "onsite": RemoteType.ONSITE,
        "on-site": RemoteType.ONSITE,
        "unknown": RemoteType.UNKNOWN,
    }

    def _normalize_remote_type(
        self,
        value: str,
    ) -> RemoteType:
        return self._REMOTE_TYPE_MAP.get(
            value.strip().lower(),
            RemoteType.UNKNOWN,
        )