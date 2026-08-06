from career_agent.models.professional_profile import (
    ProfessionalProfile,
)

from career_agent.models.cv_extraction import (
    CVExtraction,
)

from career_agent.services.professional_profile_builder import (
    ProfessionalProfileBuilder,
)
from career_agent.models.semantic_entity import (
    SemanticEntity,
)

class EmptySemanticNormalizer:

    def normalize(
        self,
        extraction,
    ):
        return []

def test_build_returns_professional_profile():

    builder = ProfessionalProfileBuilder()

    profile = builder.build(
        CVExtraction(),
    )

    assert isinstance(
        profile,
        ProfessionalProfile,
    )
    
def test_build_returns_empty_professional_profile():

    builder = ProfessionalProfileBuilder()

    profile = builder.build(
        CVExtraction(),
    )

    assert profile == ProfessionalProfile()
    
def test_build_from_empty_extraction_returns_empty_profile():

    builder = ProfessionalProfileBuilder()

    profile = builder.build(
        CVExtraction(),
    )

    assert profile == ProfessionalProfile()
    
def test_build_copies_skills_from_extraction():

    builder = ProfessionalProfileBuilder()

    extraction = CVExtraction(
        skills=[
            "Python",
            "Docker",
        ],
    )

    profile = builder.build(
        extraction,
    )

    assert profile.skills == [
        "Python",
        "Docker",
    ]
    
def test_build_copies_languages_from_extraction():

    builder = ProfessionalProfileBuilder()

    extraction = CVExtraction(
        languages=[
            "English C1",
        ],
    )

    profile = builder.build(
        extraction,
    )

    assert profile.languages == [
        "English C1",
    ]
    
def test_build_copies_knowledge_from_extraction():

    builder = ProfessionalProfileBuilder()

    extraction = CVExtraction(
        education=[
            "Computer Science",
        ],
    )

    profile = builder.build(
        extraction,
    )

    assert profile.knowledge == [
        "Computer Science",
    ]
    
