from career_agent.models.candidate_profile import (
    CandidateProfile,
)
from career_agent.repositories.candidate_profile_repository import (
    CandidateProfileRepository,
)
from pathlib import Path


def test_repository_saves_candidate_profile(
    tmp_path,
):

    repository = CandidateProfileRepository(
        tmp_path / "profile.json",
    )

    profile = CandidateProfile(
        skills=[
            "Python",
        ],
    )

    repository.save(
        profile,
    )
    
    loaded = repository.load()

    assert loaded == profile
    
def test_repository_returns_empty_profile_when_file_does_not_exist(
    tmp_path,
):

    repository = CandidateProfileRepository(
        tmp_path / "profile.json",
    )

    profile = repository.load()

    assert profile == CandidateProfile()
    
def test_repository_overwrites_candidate_profile(
    tmp_path,
):

    repository = CandidateProfileRepository(
        tmp_path / "profile.json",
    )

    repository.save(
        CandidateProfile(
            skills=[
                "Python",
            ],
        ),
    )

    repository.save(
        CandidateProfile(
            skills=[
                "Java",
            ],
        ),
    )

    loaded = repository.load()

    assert loaded.skills == [
        "Java",
    ]
    
def test_repository_exists(
    tmp_path,
):

    repository = CandidateProfileRepository(
        tmp_path / "profile.json",
    )

    assert repository.exists() is False

    repository.save(
        CandidateProfile(),
    )

    assert repository.exists() is True
    
def test_repository_delete(
    tmp_path,
):

    repository = CandidateProfileRepository(
        tmp_path / "profile.json",
    )

    repository.save(
        CandidateProfile(),
    )

    repository.delete()

    assert repository.exists() is False
    
def test_repository_persists_complete_candidate_profile(
    tmp_path,
):

    repository = CandidateProfileRepository(
        tmp_path / "profile.json",
    )

    profile = CandidateProfile(
        skills=[
            "Python",
            "Docker",
        ],
        years_experience=5,
        preferred_countries=[
            "Spain",
        ],
    )

    repository.save(
        profile,
    )

    loaded = repository.load()

    assert loaded == profile