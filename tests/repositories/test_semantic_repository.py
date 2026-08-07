from career_agent.models.cv_extraction import (
    CVExtraction,
)
from career_agent.models.semantic_entity import (
    SemanticEntity,
)
from career_agent.services.semantic_normalizer import (
    SemanticNormalizer,
)


class FakeSemanticRepository:

    def find_skill_by_label(
        self,
        label: str,
    ):

        return SemanticEntity(
            id="python",
            preferred_label="Python",
        )


def test_normalize_uses_repository():

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