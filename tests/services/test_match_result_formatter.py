from career_agent.models.candidate_profile import CandidateProfile
from career_agent.models.enums import RemoteType
from career_agent.models.job_requirements import JobRequirements
from career_agent.models.language_skill import LanguageSkill
from career_agent.models.salary_expectation import SalaryExpectation
from career_agent.services.job_matching_service import (
    JobMatchingService,
)
from career_agent.services.match_result_formatter import (
    MatchResultFormatter,
)
from tests.factories import create_job_offer


def test_formats_overall_score():

    result = JobMatchingService().match(
        create_job_offer(),
        CandidateProfile(),
    )

    formatter = MatchResultFormatter()

    text = formatter.format(
        result,
    )

    assert "Overall match:" in text
    
def test_formats_matched_requirements():

    profile = CandidateProfile(
        preferred_remote_type=RemoteType.REMOTE,
    )

    job = create_job_offer(
        remote_type=RemoteType.REMOTE,
    )

    result = JobMatchingService().match(
        job,
        profile,
    )

    formatter = MatchResultFormatter()

    text = formatter.format(
        result,
    )

    assert "Remote: 100%" in text
    assert "✓ Remote" in text
    
def test_formats_missing_requirements():

    profile = CandidateProfile(
        preferred_remote_type=RemoteType.HYBRID,
    )

    job = create_job_offer(
        remote_type=RemoteType.REMOTE,
    )

    result = JobMatchingService().match(
        job,
        profile,
    )

    formatter = MatchResultFormatter()

    text = formatter.format(
        result,
    )

    assert "Remote: 0%" in text
    assert "✗ Remote" in text
    
def test_formats_criteria_section():

    profile = CandidateProfile(
        years_experience=4,
    )

    job = create_job_offer(
        requirements=JobRequirements(
            years_experience=5,
        ),
    )

    result = JobMatchingService().match(
        job,
        profile,
    )

    formatter = MatchResultFormatter()

    text = formatter.format(
        result,
    )

    assert "Criteria" in text
    assert "Experience" in text
    
def test_formats_criterion_scores():

    profile = CandidateProfile(
        years_experience=4,
    )

    job = create_job_offer(
        requirements=JobRequirements(
            years_experience=5,
        ),
    )

    result = JobMatchingService().match(
        job,
        profile,
    )

    text = MatchResultFormatter().format(
        result,
    )

    assert "Experience: 80%" in text
    
def test_formats_skill_details():

    profile = CandidateProfile(
        skills=[
            "Python",
        ],
    )

    job = create_job_offer(
        requirements=JobRequirements(
            skills=[
                "Python",
                "Docker",
            ],
        ),
    )

    result = JobMatchingService().match(
        job,
        profile,
    )

    text = MatchResultFormatter().format(
        result,
    )

    assert "Skills: 50%" in text
    assert "✓ Python" in text
    assert "✗ Docker" in text
    
def test_formats_experience_details():

    profile = CandidateProfile(
        years_experience=4,
    )

    job = create_job_offer(
        requirements=JobRequirements(
            years_experience=5,
        ),
    )

    result = JobMatchingService().match(
        job,
        profile,
    )

    text = MatchResultFormatter().format(
        result,
    )

    assert "Experience: 80%" in text
    assert "Candidate: 4 years" in text
    assert "Required: 5 years" in text
    
def test_formats_salary_details_when_salary_matches():

    profile = CandidateProfile(
        salary=SalaryExpectation(
            amount=40000,
        ),
    )

    job = create_job_offer(
        salary=SalaryExpectation(
            amount=45000,
        ),
    )

    result = JobMatchingService().match(
        job,
        profile,
    )

    text = MatchResultFormatter().format(
        result,
    )

    assert "Salary: 100%" in text
    assert "Candidate: 40000 EUR" in text
    assert "Required: 45000 EUR" in text
    assert "✓ Salary" in text
    
def test_formats_salary_details_when_salary_does_not_match():

    profile = CandidateProfile(
        salary=SalaryExpectation(
            amount=50000,
        ),
    )

    job = create_job_offer(
        salary=SalaryExpectation(
            amount=45000,
        ),
    )

    result = JobMatchingService().match(
        job,
        profile,
    )

    text = MatchResultFormatter().format(
        result,
    )

    assert "Salary: 0%" in text
    assert "Candidate: 50000 EUR" in text
    assert "Required: 45000 EUR" in text
    assert "✗ Salary" in text
    
def test_formats_language_details_when_language_matches():

    profile = CandidateProfile(
        languages=[
            LanguageSkill(
                language="English",
                level="C2",
            ),
        ],
    )

    job = create_job_offer(
        requirements=JobRequirements(
            languages=[
                LanguageSkill(
                    language="English",
                    level="C1",
                ),
            ],
        ),
    )

    result = JobMatchingService().match(
        job,
        profile,
    )

    text = MatchResultFormatter().format(
        result,
    )

    assert "Languages: 100%" in text
    assert "Candidate: English C2" in text
    assert "Required: English C1" in text
    assert "✓ English" in text
    
def test_formats_language_details_when_language_does_not_match():

    profile = CandidateProfile(
        languages=[
            LanguageSkill(
                language="English",
                level="B2",
            ),
        ],
    )

    job = create_job_offer(
        requirements=JobRequirements(
            languages=[
                LanguageSkill(
                    language="English",
                    level="C1",
                ),
            ],
        ),
    )

    result = JobMatchingService().match(
        job,
        profile,
    )

    text = MatchResultFormatter().format(
        result,
    )

    assert "Languages: 0%" in text
    assert "Candidate: English B2" in text
    assert "Required: English C1" in text
    assert "✗ English" in text