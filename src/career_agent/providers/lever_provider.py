from career_agent.collectors.lever_collector import LeverCollector
from career_agent.parsers.lever_parser import LeverParser

from .ats_provider import ATSProvider


def lever_provider() -> ATSProvider:
    return ATSProvider(
        collector=LeverCollector(),
        parser=LeverParser(),
    )