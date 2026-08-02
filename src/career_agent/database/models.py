from datetime import datetime

from sqlmodel import Field, SQLModel


class JobOfferRecord(SQLModel, table=True):

    id: str = Field(primary_key=True)

    source: str

    url: str

    title: str

    company_name: str

    description: str

    location: str

    employment_type: str | None = None

    remote_type: str | None = None
    
    salary_amount: int | None = Field(default=None)

    created_at: datetime