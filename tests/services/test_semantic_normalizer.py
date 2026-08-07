from career_agent.models.cv_extraction import (
    CVExtraction,
)

from career_agent.services.semantic_normalizer import (
    SemanticNormalizer,
)
from career_agent.models.semantic_entity import (
    SemanticEntity,
)
class EmptySemanticRepository:

    def find_skill_by_label(
        self,
        label: str,
    ):
        return None

def test_normalize_returns_list():

    repository = FakeSemanticRepository()

    normalizer = SemanticNormalizer(
        repository,
    )

    result = normalizer.normalize(
        CVExtraction(),
    )

    assert isinstance(
        result,
        list,
    )
    
def test_normalize_empty_extraction_returns_empty_list():

    normalizer = SemanticNormalizer(
        EmptySemanticRepository(),
    )
    result = normalizer.normalize(
        CVExtraction(),
    )

    assert result == []
    
class FakeSemanticRepository:

    def find_skill_by_label(
        self,
        label: str,
    ) -> SemanticEntity | None:

        return SemanticEntity(
            id="python",
            preferred_label="Python",
        )


def test_normalize_skill():

    repository = FakeSemanticRepository()

    normalizer = SemanticNormalizer(
        repository,
    )

    entities = normalizer.normalize(
        CVExtraction(
            skills=[
                "Python",
            ],
        ),
    )

    assert entities == [
        SemanticEntity(
            id="python",
            preferred_label="Python",
        ),
    ]