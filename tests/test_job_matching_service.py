from career_agent.models.candidate_profile import (
    CandidateProfile,
)
from career_agent.services.job_matching_service import (
    JobMatchingService,
)
from career_agent.testing.factories import (
    create_job_offer,
)
from career_agent.models.salary_expectation import (
    SalaryExpectation,
)
from career_agent.models.enums import RemoteType

def test_match_returns_score():

    service = JobMatchingService()

    profile = CandidateProfile()

    job = create_job_offer()

    result = service.match(
        job,
        profile,
    )

    assert result.score == 0.0
    
def test_match_scores_one_when_remote_type_matches():

    profile = CandidateProfile(
        preferred_remote_type=RemoteType.REMOTE,
    )

    job = create_job_offer(
        remote_type=RemoteType.REMOTE,
    )

    service = JobMatchingService()

    result = service.match(
        job,
        profile,
    )

    assert result.score == 1.0
    
def test_match_scores_zero_when_remote_type_differs():

    profile = CandidateProfile(
        preferred_remote_type=RemoteType.REMOTE,
    )

    job = create_job_offer(
        remote_type=RemoteType.ONSITE,
    )

    service = JobMatchingService()

    result = service.match(
        job,
        profile,
    )

    assert result.score == 0.0
    
def test_match_scores_zero_when_candidate_has_no_remote_preference():

    profile = CandidateProfile()

    job = create_job_offer(
        remote_type=RemoteType.REMOTE,
    )

    result = JobMatchingService().match(
        job,
        profile,
    )

    assert result.score == 0.0
    
def test_match_scores_one_when_country_matches():

    profile = CandidateProfile(
        preferred_countries=[
            "Spain",
            "Portugal",
        ],
    )

    job = create_job_offer(
        location="Madrid, Spain",
    )

    result = JobMatchingService().match(
        job,
        profile,
    )

    assert result.score == 1.0
    
def test_match_scores_zero_when_country_does_not_match():

    profile = CandidateProfile(
        preferred_countries=[
            "Germany",
        ],
    )

    job = create_job_offer(
        location="Madrid, Spain",
    )

    result = JobMatchingService().match(
        job,
        profile,
    )

    assert result.score == 0.0
    
def test_match_scores_zero_when_candidate_has_no_preferred_countries():

    profile = CandidateProfile()

    job = create_job_offer(
        location="Madrid, Spain",
    )

    result = JobMatchingService().match(
        job,
        profile,
    )

    assert result.score == 0.0
    
def test_match_scores_one_when_salary_matches():

    profile = CandidateProfile(
        salary=SalaryExpectation(
            amount=60000,
        ),
    )

    job = create_job_offer(
        salary=SalaryExpectation(
            amount=70000,
        ),
    )

    result = JobMatchingService().match(
        job,
        profile,
    )

    assert result.score == 1.0
    
def test_match_scores_zero_when_salary_is_too_low():

    profile = CandidateProfile(
        salary=SalaryExpectation(
            amount=70000,
        ),
    )

    job = create_job_offer(
        salary=SalaryExpectation(
            amount=60000,
        ),
    )

    result = JobMatchingService().match(
        job,
        profile,
    )

    assert result.score == 0.0
    
def test_match_scores_zero_when_job_has_no_salary():

    profile = CandidateProfile(
        salary=SalaryExpectation(
            amount=60000,
        ),
    )

    job = create_job_offer(
        salary=None,
    )

    result = JobMatchingService().match(
        job,
        profile,
    )

    assert result.score == 0.0
    
def test_match_scores_zero_when_candidate_has_no_salary_expectation():

    profile = CandidateProfile()

    job = create_job_offer(
        salary=SalaryExpectation(
            amount=70000,
        ),
    )

    result = JobMatchingService().match(
        job,
        profile,
    )

    assert result.score == 0.0