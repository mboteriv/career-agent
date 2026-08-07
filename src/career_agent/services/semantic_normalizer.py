from career_agent.models.cv_extraction import (
    CVExtraction,
)
from career_agent.models.semantic_entity import (
    SemanticEntity,
)
from career_agent.repositories.semantic_repository import (
    SemanticRepository,
)


class SemanticNormalizer:
    def __init__(
        self,
        repository: SemanticRepository,
    ):
        self._repository = repository

    def normalize(
        self,
        extraction: CVExtraction,
    ) -> list[SemanticEntity]:

        entities = []

        for skill in extraction.skills:

            entity = self._repository.find_skill_by_label(
                skill,
            )
            if entity is not None:
                entities.append(entity)

        return entities