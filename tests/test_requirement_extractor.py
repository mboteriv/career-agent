from career_agent.models.language_skill import LanguageSkill
from career_agent.services.requirement_extractor import (
    RequirementExtractor,
)


def test_empty_description_returns_empty_requirements():

    extractor = RequirementExtractor()

    requirements = extractor.extract("")

    assert requirements.skills == []
    assert requirements.languages == []
    assert requirements.years_experience is None
    
def test_extract_python_skill():

    extractor = RequirementExtractor()

    requirements = extractor.extract(
        "We are looking for a Python developer.",
    )

    assert requirements.skills == [
        "Python",
    ]
    
def test_extract_multiple_skills():

    extractor = RequirementExtractor()

    requirements = extractor.extract(
        "Python, Docker and Kubernetes required.",
    )

    assert requirements.skills == [
        "Python",
        "Docker",
        "Kubernetes",
    ]
    
def test_extract_kubernetes_from_k8s():

    extractor = RequirementExtractor()

    requirements = extractor.extract(
        "Experience with K8s required.",
    )

    assert requirements.skills == [
        "Kubernetes",
    ]
    
    
def test_extract_multiple_languages():

    extractor = RequirementExtractor()

    requirements = extractor.extract(
        "English and Spanish required.",
    )

    assert requirements.languages == [
        LanguageSkill(
            language="English",
            level="Unknown",
        ),
        LanguageSkill(
            language="Spanish",
            level="Unknown",
        ),
    ]
    
def test_extract_english_c1():

    extractor = RequirementExtractor()

    requirements = extractor.extract(
        "English C1 required.",
    )

    assert requirements.languages[0].level == "C1"
    
def test_extract_fluent_english():

    extractor = RequirementExtractor()

    requirements = extractor.extract(
        "Fluent English required.",
    )

    assert requirements.languages[0].level == "Fluent"
    
def test_extract_native_english():

    extractor = RequirementExtractor()

    requirements = extractor.extract(
        "Native English speaker.",
    )

    assert requirements.languages[0].level == "Native"
    
def test_extract_unknown_language_level():

    extractor = RequirementExtractor()

    requirements = extractor.extract(
        "English required.",
    )

    assert requirements.languages[0].level == "Unknown"
    
def test_extract_years_experience():

    extractor = RequirementExtractor()

    requirements = extractor.extract(
        "3 years of experience required.",
    )

    assert requirements.years_experience == 3
    
def test_extract_years_experience_with_plus():

    extractor = RequirementExtractor()

    requirements = extractor.extract(
        "5+ years of experience required.",
    )

    assert requirements.years_experience == 5
    
def test_extract_no_experience():

    extractor = RequirementExtractor()

    requirements = extractor.extract(
        "Experience preferred.",
    )

    assert requirements.years_experience is None