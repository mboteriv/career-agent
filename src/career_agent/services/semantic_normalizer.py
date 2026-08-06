from career_agent.models.cv_extraction import CVExtraction
from career_agent.models.semantic_entity import SemanticEntity


class SemanticNormalizer:

    def normalize(
        self,
        extraction: CVExtraction,
    ) -> list[SemanticEntity]:

        entities = []

        for skill in extraction.skills:

            entities.append(
                SemanticEntity(
                    id=skill.lower(),
                    preferred_label=skill,
                )
            )

        return entities