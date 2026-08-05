from unittest import result

from career_agent.models.candidate_profile import (
    CandidateProfile,
)
from career_agent.models.job_requirements import JobRequirements
from career_agent.models.language_skill import LanguageSkill
from career_agent.services.job_matching_service import (
    JobMatchingService,
)
from tests.factories import (
    create_job_offer,
)
from career_agent.models.salary_expectation import (
    SalaryExpectation,
)
from career_agent.models.enums import RemoteType
from career_agent.models.criterion_match import CriterionMatch
from career_agent.models.matching_criterion import MatchingCriterion
from career_agent.models.matching_policy import MatchingPolicy

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
    
def test_match_scores_one_when_all_skills_match():

    profile = CandidateProfile(
        skills=[
            "Python",
            "Docker",
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

    assert result.score == 1.0
    
def test_match_scores_partial_when_some_skills_match():

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

    assert result.score == 0.5
    
def test_match_scores_zero_when_no_skills_match():

    profile = CandidateProfile(
        skills=[
            "Java",
        ],
    )

    job = create_job_offer(
        requirements=JobRequirements(
            skills=[
                "Python",
            ],
        ),
    )

    result = JobMatchingService().match(
        job,
        profile,
    )

    assert result.score == 0.0
    
def test_match_scores_one_when_languages_match():

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

    assert result.score == 1.0
    
def test_match_scores_one_when_experience_matches():

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

    assert result.score == 1.0
    
def test_match_scores_zero_when_experience_is_insufficient():

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

    assert result.score == 0.0
    
def test_match_scores_zero_when_job_has_no_experience_requirement():

    profile = CandidateProfile(
        years_experience=10,
    )

    job = create_job_offer()

    result = JobMatchingService().match(
        job,
        profile,
    )

    assert result.score == 0.0
    
def test_match_result_contains_job():

    job = create_job_offer()

    result = JobMatchingService().match(
        job,
        CandidateProfile(),
    )

    assert result.job == job
    
def test_match_result_contains_matched_skills():

    profile = CandidateProfile(
        skills=[
            "Python",
            "Docker",
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

    assert "Python" in result.matched_requirements
    assert "Docker" in result.matched_requirements
    
def test_match_result_contains_missing_skills():

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

    assert "Python" in result.matched_requirements
    assert "Docker" in result.missing_requirements
    
def test_build_criterion_matches():

    service = JobMatchingService()

    job = create_job_offer(
        description="Python required.",
    )

    profile = CandidateProfile(
        skills=["Python"],
    )

    results = service._build_criterion_matches(
        job,
        profile,
    )

    assert len(results) == 6

    assert all(
        isinstance(
            result,
            CriterionMatch,
        )
        for result in results
    )

    assert results[0].criterion == MatchingCriterion.REMOTE
    assert results[1].criterion == MatchingCriterion.COUNTRY
    assert results[2].criterion == MatchingCriterion.SALARY
    assert results[3].criterion == MatchingCriterion.SKILLS
    assert results[4].criterion == MatchingCriterion.LANGUAGES
    assert results[5].criterion == MatchingCriterion.EXPERIENCE
    
def test_skill_matches_returns_required_and_matched_skills():

    service = JobMatchingService()

    job = create_job_offer(
        requirements=JobRequirements(
            skills=[
                "Python",
                "Docker",
            ],
        ),
    )

    profile = CandidateProfile(
        skills=[
            "Python",
            "Git",
        ],
    )

    required, matched = service._skill_matches(
        job,
        profile,
    )

    assert required == {
        "Python",
        "Docker",
    }

    assert matched == {
        "Python",
    }
    
def test_build_skills_criterion_match():

    service = JobMatchingService()

    job = create_job_offer(
        requirements=JobRequirements(
            skills=[
                "Python",
                "Docker",
            ],
        ),
    )

    profile = CandidateProfile(
        skills=[
            "Python",
            "Git",
        ],
    )

    result = service._build_skills_criterion_match(
        job,
        profile,
    )

    assert result.criterion == MatchingCriterion.SKILLS
    assert result.score == 0.5
    
def test_build_skills_criterion_match_contains_explanations():

    service = JobMatchingService()

    job = create_job_offer(
        requirements=JobRequirements(
            skills=[
                "Python",
                "Docker",
            ],
        ),
    )

    profile = CandidateProfile(
        skills=[
            "Python",
            "Git",
        ],
    )

    result = service._build_skills_criterion_match(
        job,
        profile,
    )

    assert set(result.matched) == {"Python"}
    assert set(result.missing) == {"Docker"}
    
def test_find_criterion_match():

    service = JobMatchingService()

    criterion_matches = [
        CriterionMatch(
            criterion=MatchingCriterion.SKILLS,
            score=1.0,
        ),
    ]

    result = service._find_criterion_match(
        criterion_matches,
        MatchingCriterion.SKILLS,
    )

    assert result.criterion == MatchingCriterion.SKILLS
    
def test_build_skills_criterion_match_is_not_applicable_when_no_skills_required():

    service = JobMatchingService()

    job = create_job_offer(
        requirements=JobRequirements(
            skills=[],
        ),
    )

    profile = CandidateProfile(
        skills=[
            "Python",
        ],
    )

    result = service._build_skills_criterion_match(
        job,
        profile,
    )

    assert result.applicable is False
    
def test_build_skills_criterion_match_is_applicable_when_skills_required():

    service = JobMatchingService()

    job = create_job_offer(
        requirements=JobRequirements(
            skills=[
                "Python",
            ],
        ),
    )

    profile = CandidateProfile()

    result = service._build_skills_criterion_match(
        job,
        profile,
    )

    assert result.applicable is True
    
def test_remote_criterion_is_applicable_when_candidate_has_preference():

    service = JobMatchingService()

    job = create_job_offer(
        remote_type=RemoteType.REMOTE,
    )

    profile = CandidateProfile(
        preferred_remote_type=RemoteType.REMOTE,
    )

    result = service._find_criterion_match(
        service._build_criterion_matches(
            job,
            profile,
        ),
        MatchingCriterion.REMOTE,
    )

    assert result.applicable is True
    
def test_remote_criterion_is_not_applicable_when_candidate_has_no_preference():

    service = JobMatchingService()

    job = create_job_offer(
        remote_type=RemoteType.REMOTE,
    )

    profile = CandidateProfile()

    result = service._find_criterion_match(
        service._build_criterion_matches(
            job,
            profile,
        ),
        MatchingCriterion.REMOTE,
    )

    assert result.applicable is False
    
def test_country_criterion_is_applicable_when_candidate_has_preferred_countries():

    service = JobMatchingService()

    job = create_job_offer(
        location="Spain",
    )

    profile = CandidateProfile(
        preferred_countries=[
            "Spain",
        ],
    )

    result = service._find_criterion_match(
        service._build_criterion_matches(
            job,
            profile,
        ),
        MatchingCriterion.COUNTRY,
    )

    assert result.applicable is True
    
def test_country_criterion_is_not_applicable_when_candidate_has_no_preferred_countries():

    service = JobMatchingService()

    job = create_job_offer(
        location="Spain",
    )

    profile = CandidateProfile()

    result = service._find_criterion_match(
        service._build_criterion_matches(
            job,
            profile,
        ),
        MatchingCriterion.COUNTRY,
    )

    assert result.applicable is False
    
def test_salary_criterion_is_applicable_when_candidate_and_job_have_salary():

    service = JobMatchingService()

    job = create_job_offer(
        salary=SalaryExpectation(
            amount=60000,
        ),
    )

    profile = CandidateProfile(
        salary=SalaryExpectation(
            amount=50000,
        ),
    )

    result = service._find_criterion_match(
        service._build_criterion_matches(
            job,
            profile,
        ),
        MatchingCriterion.SALARY,
    )

    assert result.applicable is True
    
def test_salary_criterion_is_not_applicable_when_job_has_no_salary():

    service = JobMatchingService()

    job = create_job_offer(
        salary=None,
    )

    profile = CandidateProfile(
        salary=SalaryExpectation(
            amount=50000,
        ),
    )

    result = service._find_criterion_match(
        service._build_criterion_matches(
            job,
            profile,
        ),
        MatchingCriterion.SALARY,
    )

    assert result.applicable is False
    
def test_salary_criterion_is_not_applicable_when_candidate_has_no_salary():

    service = JobMatchingService()

    job = create_job_offer(
        salary=SalaryExpectation(
         amount=60000,
        ),
    )

    profile = CandidateProfile()

    result = service._find_criterion_match(
        service._build_criterion_matches(
            job,
            profile,
        ),
        MatchingCriterion.SALARY,
    )

    assert result.applicable is False
    
def test_salary_criterion_is_not_applicable_when_neither_has_salary():

    service = JobMatchingService()

    job = create_job_offer(
        salary=None,
    )

    profile = CandidateProfile()

    result = service._find_criterion_match(
        service._build_criterion_matches(
            job,
            profile,
        ),
        MatchingCriterion.SALARY,
    )

    assert result.applicable is False
    
def test_languages_criterion_is_applicable_when_job_requires_languages():

    service = JobMatchingService()

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

    profile = CandidateProfile()

    result = service._find_criterion_match(
        service._build_criterion_matches(
            job,
            profile,
        ),
        MatchingCriterion.LANGUAGES,
    )

    assert result.applicable is True
    
def test_languages_criterion_is_not_applicable_when_job_requires_no_languages():

    service = JobMatchingService()

    job = create_job_offer(
        requirements=JobRequirements(),
    )

    profile = CandidateProfile()

    result = service._find_criterion_match(
        service._build_criterion_matches(
            job,
            profile,
        ),
        MatchingCriterion.LANGUAGES,
    )

    assert result.applicable is False
    
def test_experience_criterion_is_applicable_when_job_requires_experience():

    service = JobMatchingService()

    job = create_job_offer(
        requirements=JobRequirements(
            years_experience=3,
        ),
    )

    profile = CandidateProfile(
        years_experience=5,
    )

    result = service._find_criterion_match(
        service._build_criterion_matches(
            job,
            profile,
        ),
        MatchingCriterion.EXPERIENCE,
    )

    assert result.applicable is True
    
def test_experience_criterion_is_not_applicable_when_job_requires_no_experience():

    service = JobMatchingService()

    job = create_job_offer(
        requirements=JobRequirements(),
    )

    profile = CandidateProfile(
        years_experience=5,
    )

    result = service._find_criterion_match(
        service._build_criterion_matches(
            job,
            profile,
        ),
        MatchingCriterion.EXPERIENCE,
    )

    assert result.applicable is False