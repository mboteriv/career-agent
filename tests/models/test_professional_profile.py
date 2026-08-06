from career_agent.models.professional_profile import (
    ProfessionalProfile,
)


def test_create_empty_professional_profile():

    profile = ProfessionalProfile()

    assert profile.occupations == []
    assert profile.capabilities == []
    assert profile.skills == []
    assert profile.knowledge == []
    assert profile.languages == []


def test_create_professional_profile():

    profile = ProfessionalProfile(
        occupations=[
            "Translator",
        ],
        capabilities=[
            "Localization",
        ],
        skills=[
            "MemoQ",
            "Python",
        ],
        knowledge=[
            "Translation Theory",
        ],
        languages=[
            "English C2",
        ],
    )

    assert profile.occupations == [
        "Translator",
    ]

    assert profile.capabilities == [
        "Localization",
    ]

    assert profile.skills == [
        "MemoQ",
        "Python",
    ]

    assert profile.knowledge == [
        "Translation Theory",
    ]

    assert profile.languages == [
        "English C2",
    ]
    
