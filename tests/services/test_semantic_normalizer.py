from career_agent.models.cv_extraction import (
    CVExtraction,
)

from career_agent.models.semantic_entity import SemanticEntity
from career_agent.services.semantic_normalizer import (
    SemanticNormalizer,
)


def test_normalize_returns_list():

    normalizer = SemanticNormalizer()

    result = normalizer.normalize(
        CVExtraction(),
    )

    assert isinstance(
        result,
        list,
    )
    
def test_normalize_empty_extraction_returns_empty_list():

    normalizer = SemanticNormalizer()

    result = normalizer.normalize(
        CVExtraction(),
    )

    assert result == []
    
def test_normalize_skill():

    extraction = CVExtraction(
        skills=[
            "Python",
        ],
    )

    entities = SemanticNormalizer().normalize(
        extraction,
    )

    assert entities == [
        SemanticEntity(
            id="python",
            preferred_label="Python",
        ),
    ]