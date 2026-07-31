from career_agent.collectors.greenhouse_collector import GreenhouseCollector
from career_agent.parsers.greenhouse_parser import GreenhouseParser

from .ats_provider import ATSProvider


def greenhouse_provider() -> ATSProvider:
    return ATSProvider(
        collector=GreenhouseCollector(),
        parser=GreenhouseParser(),
    )