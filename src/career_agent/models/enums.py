from enum import Enum


class Source(str, Enum):
    """Supported job sources."""

    GREENHOUSE = "greenhouse"
    LEVER = "lever"

class EmploymentType(str, Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    INTERN = "intern"
    TEMPORARY = "temporary"
    OTHER = "other"

class RemoteType(str, Enum):
    REMOTE = "remote"
    HYBRID = "hybrid"
    ONSITE = "onsite"
    UNKNOWN = "unknown"