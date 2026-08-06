from career_agent.models.cv_extraction import (
    CVExtraction,
)


def test_create_empty_cv_extraction():

    extraction = CVExtraction()

    assert extraction.summary == ""

    assert extraction.experience == []

    assert extraction.education == []

    assert extraction.skills == []

    assert extraction.languages == []


def test_create_cv_extraction():

    extraction = CVExtraction(
        summary=(
            "Experienced software engineer."
        ),
        experience=[
            (
                "Developed REST APIs using "
                "Python and FastAPI."
            ),
        ],
        education=[
            (
                "Bachelor of Computer Science"
            ),
        ],
        skills=[
            "Python",
            "Docker",
        ],
        languages=[
            "English C1",
            "Spanish Native",
        ],
    )

    assert extraction.summary == (
        "Experienced software engineer."
    )

    assert extraction.experience == [
        (
            "Developed REST APIs using "
            "Python and FastAPI."
        ),
    ]

    assert extraction.education == [
        (
            "Bachelor of Computer Science"
        ),
    ]

    assert extraction.skills == [
        "Python",
        "Docker",
    ]

    assert extraction.languages == [
        "English C1",
        "Spanish Native",
    ]