from dataclasses import dataclass


@dataclass(frozen=True)
class ATSProvider:
    collector: object
    parser: object