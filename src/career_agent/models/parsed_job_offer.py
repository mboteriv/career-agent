from pydantic import BaseModel, ConfigDict

from career_agent.models.enums import Source


class ParsedJobOffer(BaseModel):
    """Job offer extracted from a provider but not yet normalized."""

    model_config = ConfigDict(frozen=True)

    # Identity

    id: str
    source: Source
    url: str

    # Business data

    title: str
    company_name: str
    description: str
    location: str

    # Values to normalize

    employment_type: str | None = None
    remote_type: str | None = None