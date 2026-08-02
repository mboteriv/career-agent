from career_agent.dto.parsed_job_offer import ParsedJobOffer
from career_agent.models.enums import (
    EmploymentType,
    RemoteType,
)
from career_agent.models.job_offer import JobOffer
from career_agent.normalizers.job_offer_normalizer import JobOfferNormalizer

from datetime import datetime
from career_agent.models.enums import Source


def create_parsed_job_offer(**kwargs):
    data = {
        "id": "123",
        "source": Source.GREENHOUSE,
        "collected_at": datetime.now(),
        "title": "Backend Engineer",
        "company_name": "Example Inc.",
        "description": "Example description",
        "location": "Málaga, Spain",
        "employment_type": "Full Time",
        "remote_type": "Hybrid",
        "source_url": "https://example.com/job/123",
    }

    data.update(kwargs)
    return ParsedJobOffer(**data)


def test_normalizer_creates_job_offer():
    parsed = create_parsed_job_offer()

    normalizer = JobOfferNormalizer()

    job = normalizer.normalize(parsed)

    assert isinstance(job, JobOffer)
    assert job.title == parsed.title
    assert job.company_name == parsed.company_name

def test_permanent_maps_to_full_time():
    parsed = create_parsed_job_offer(
    employment_type="Permanent"
 )

    job = JobOfferNormalizer().normalize(parsed)

    assert job.employment_type == EmploymentType.FULL_TIME

def test_full_time_maps_to_full_time():
    parsed = create_parsed_job_offer(
    employment_type="Full Time"
)

    job = JobOfferNormalizer().normalize(parsed)

    assert job.employment_type == EmploymentType.FULL_TIME

def test_intern_maps_to_intern():
    parsed = create_parsed_job_offer(
    employment_type="Intern"
)

    job = JobOfferNormalizer().normalize(parsed)

    assert job.employment_type == EmploymentType.INTERN

def test_unknown_employment_type_maps_to_other():
    parsed = create_parsed_job_offer(
    employment_type="Whatever"
)

    job = JobOfferNormalizer().normalize(parsed)

    assert job.employment_type == EmploymentType.OTHER

def test_remote_maps_to_remote():
    parsed = create_parsed_job_offer(
        remote_type="Remote"
    )

    job = JobOfferNormalizer().normalize(parsed)

    assert job.remote_type == RemoteType.REMOTE

def test_hybrid_maps_to_hybrid():
    parsed = create_parsed_job_offer(
    remote_type="Hybrid"
    )

    job = JobOfferNormalizer().normalize(parsed)

    assert job.remote_type == RemoteType.HYBRID

def test_onsite_maps_to_onsite():
    parsed = create_parsed_job_offer(
    remote_type="Onsite"
    )

    job = JobOfferNormalizer().normalize(parsed)

    assert job.remote_type == RemoteType.ONSITE

def test_unknown_remote_type_maps_to_unknown():
    parsed = create_parsed_job_offer(
    remote_type="Whatever"
    )

    job = JobOfferNormalizer().normalize(parsed)

    assert job.remote_type == RemoteType.UNKNOWN

def test_on_site_maps_to_onsite():
    parsed = create_parsed_job_offer(
        remote_type="On-Site"
    )

    job = JobOfferNormalizer().normalize(parsed)

    assert job.remote_type == RemoteType.ONSITE
    
def test_normalizer_infers_remote_type_from_home_based_location():

    parsed = create_parsed_job_offer(
        location="Home based - EMEA",
        remote_type=None,
    )

    normalizer = JobOfferNormalizer()

    job = normalizer.normalize(parsed)

    assert job.remote_type == RemoteType.REMOTE
    
def test_normalizer_preserves_existing_remote_type():

    parsed = create_parsed_job_offer(
        location="Home based - EMEA",
        remote_type="hybrid",
    )

    normalizer = JobOfferNormalizer()

    job = normalizer.normalize(parsed)

    assert job.remote_type == RemoteType.HYBRID