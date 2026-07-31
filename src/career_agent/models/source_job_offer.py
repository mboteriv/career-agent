from typing import Any

from pydantic import BaseModel, ConfigDict

from career_agent.models.enums import Source


class SourceJobOffer(BaseModel):
    """Raw job offer received from an external provider."""

    model_config = ConfigDict(frozen=True)

    source: Source
    raw_data: dict
    metadata: dict[str, Any] = {}