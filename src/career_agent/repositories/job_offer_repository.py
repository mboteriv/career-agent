from requests import session

from career_agent.database.database import get_session
from career_agent.database.models import JobOfferRecord
from sqlalchemy import delete
from career_agent.models import job_offer
from career_agent.models.job_offer import JobOffer
from career_agent.models.enums import (
    EmploymentType,
    RemoteType,
    Source,
)
from sqlmodel import select



class JobOfferRepository:

    def save(self, job_offer):
        with get_session() as session:

            session.add(
                self._to_record(job_offer)
            )

            session.commit()

    def _to_record(
        self,
        job_offer,
    ) -> JobOfferRecord:

        return JobOfferRecord(
            id=f"{job_offer.source.value}:{job_offer.id}",
            source=job_offer.source.value,
            url=job_offer.url,
            title=job_offer.title,
            company_name=job_offer.company_name,
            description=job_offer.description,
            location=job_offer.location,
            employment_type=(
                job_offer.employment_type.value
                if job_offer.employment_type
                else None
            ),
            remote_type=(
                job_offer.remote_type.value
                if job_offer.remote_type
                else None
            ),
            created_at=job_offer.created_at,
        )

    def _to_domain(
        self,
        record: JobOfferRecord,
    ) -> JobOffer:

        return JobOffer(
            id=record.id.split(":", 1)[1],
            source=Source(record.source),
            url=record.url,
            title=record.title,
            company_name=record.company_name,
            description=record.description,
            location=record.location,
            employment_type=(
                EmploymentType(record.employment_type)
                if record.employment_type
                else None
            ),
            remote_type=(
                RemoteType(record.remote_type)
                if record.remote_type
                else None
            ),
            created_at=record.created_at,
        )

    def get_by_id(
        self,
        source,
        job_id,
    ):
        with get_session() as session:
            record_id = f"{source.value}:{job_id}"

            record = session.get(
                JobOfferRecord,
                record_id,
            )

            if record is None:
                return None

            return self._to_domain(record)

    def delete_all(self):
        with get_session() as session:
            session.exec(
                delete(JobOfferRecord)
            )
            session.commit()

    def list_all(self):
        with get_session() as session:
            records = session.exec(
                select(JobOfferRecord)
            ).all()

            return [
                self._to_domain(record)
                for record in records
            ]

    def exists(
        self,
        source,
        job_id,
    ):
        return (
            self.get_by_id(source, job_id)
            is not None
        )

    def save_all(
        self,
        job_offers,
    ):
        for job_offer in job_offers:
            self.save(job_offer)

    def update(
        self,
        job_offer: JobOffer,
    ) -> None:

        with get_session() as session:

            record_id = f"{job_offer.source.value}:{job_offer.id}"

            record = session.get(
                JobOfferRecord,
                record_id,
            )

            if record is None:
                return

            record.url = job_offer.url
            record.title = job_offer.title
            record.company_name = job_offer.company_name
            record.description = job_offer.description
            record.location = job_offer.location

            record.employment_type = (
                job_offer.employment_type.value
                if job_offer.employment_type
                else None
            )

            record.remote_type = (
                job_offer.remote_type.value
                if job_offer.remote_type
                else None
            )

            record.created_at = job_offer.created_at

            session.add(record)
            session.commit()

    def list_by_source(
        self,
        source: Source,
    )-> list[JobOffer]:

        with get_session() as session:

            records = session.exec(
                select(JobOfferRecord).where(
                    JobOfferRecord.source == source.value
                )
            ).all()

            return [
                self._to_domain(record)
                for record in records
            ]

    def delete(
        self,
        source: Source,
        job_id: str,
    ) -> None:

        with get_session() as session:

            record_id = (
                f"{source.value}:{job_id}"
            )

            record = session.get(
                JobOfferRecord,
                record_id,
            )

            if record is None:
                return

            session.delete(record)
            session.commit()