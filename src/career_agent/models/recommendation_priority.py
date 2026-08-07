from enum import StrEnum


class RecommendationPriority(StrEnum):
    """Priority assigned to a recommended skill."""

    ESSENTIAL = "essential"

    OPTIONAL = "optional"