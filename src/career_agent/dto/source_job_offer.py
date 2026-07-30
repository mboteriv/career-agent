from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict

from career_agent.models.enums import Source


class SourceJobOffer(BaseModel):
    """Raw job offer collected from an external source."""

    model_config = ConfigDict(frozen=True)

    source: Source
    payload: dict[str, Any]
    collected_at: datetime