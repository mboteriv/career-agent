from career_agent.models.candidate_profile import CandidateProfile
from career_agent.models.criterion_match import CriterionMatch
from career_agent.models.enums import RemoteType
from career_agent.models.job_requirements import JobRequirements
from career_agent.models.language_skill import LanguageSkill
from career_agent.models.match_result import MatchResult
import pytest
from pydantic import ValidationError

from career_agent.models.matching_criterion import MatchingCriterion
from career_agent.services.job_matching_service import JobMatchingService
from tests.factories import create_job_offer
from career_agent.models.salary_expectation import (
    SalaryExpectation,
)



def test_create_match_result():

    result = MatchResult(
        job=create_job_offer(),
        score=0.75,
    )

    assert result.score == 0.75
    
def test_match_result_is_immutable():

    result = MatchResult(
        job=create_job_offer(),
        score=0.75,
    )

    with pytest.raises(ValidationError):
        result.score = 1.0
        
def test_match_result_contains_empty_explanations():

    result = JobMatchingService().match(
        create_job_offer(),
        CandidateProfile(),
    )

    assert result.matched_requirements == []
    assert result.missing_requirements == []
    
def test_match_result_contains_matched_remote_requirement():

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

    assert result.matched_requirements == [
        "Remote",
    ]

    assert result.missing_requirements == []
    
def test_match_result_contains_missing_remote_requirement():

    profile = CandidateProfile(
        preferred_remote_type=RemoteType.REMOTE,
    )

    job = create_job_offer(
        remote_type=RemoteType.ONSITE,
    )

    result = JobMatchingService().match(
        job,
        profile,
    )

    assert result.matched_requirements == []

    assert result.missing_requirements == [
        "Remote",
    ]
    
def test_match_result_contains_matched_languages():

    profile = CandidateProfile(
        languages=[
            LanguageSkill(
                language="English",
                level="C1",
            ),
        ],
    )

    job = create_job_offer(
        requirements=JobRequirements(
            languages=[
                LanguageSkill(
                    language="English",
                    level="B2",
                ),
            ],
        ),
    )

    result = JobMatchingService().match(
        job,
        profile,
    )

    assert "English" in result.matched_requirements
    
def test_match_result_contains_missing_languages():

    profile = CandidateProfile(
        languages=[
            LanguageSkill(
                language="Spanish",
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

    assert "English" in result.missing_requirements
    
def test_match_result_contains_matched_experience():

    profile = CandidateProfile(
        years_experience=5,
    )

    job = create_job_offer(
        requirements=JobRequirements(
            years_experience=3,
        ),
    )

    result = JobMatchingService().match(
        job,
        profile,
    )

    assert "Experience" in result.matched_requirements
    
def test_match_result_contains_missing_experience():

    profile = CandidateProfile(
        years_experience=2,
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

    assert "Experience" in result.missing_requirements
    
def test_match_result_contains_matched_salary():

    profile = CandidateProfile(
        salary=SalaryExpectation(
            amount=50000,
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

    assert "Salary" in result.matched_requirements
    
def test_match_result_contains_missing_salary():

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

    assert "Salary" in result.missing_requirements
    
def test_match_result_contains_criterion_matches():

    criterion_matches = [
        CriterionMatch(
            criterion=MatchingCriterion.SKILLS,
            score=1.0,
            matched=[
                "Python",
            ],
        ),
    ]

    result = MatchResult(
        job=create_job_offer(),
        score=1.0,
        criterion_matches=criterion_matches,
        matched_requirements=[
            "Python",
        ],
        missing_requirements=[],
    )

    assert result.criterion_matches == criterion_matches