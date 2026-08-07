from typing import Protocol

from career_agent.models.semantic_entity import (
    SemanticEntity,
)



class SemanticRepository(Protocol):

    def find_skill(
        self,
        label: str,
    ) -> SemanticEntity | None:
        for skill in extraction.skills:
            entities.append(
                SemanticEntity(
                    id=skill.lower(),
                    preferred_label=skill,
                )
            )
            
    def find_skill_by_label(
        self,
        label: str,
    ) -> SemanticEntity | None:
        ...

    def find_skill_by_alias(
        self,
        alias: str,
    ) -> SemanticEntity | None:
        ...

    def find_skills_for_occupation(
        self,
        occupation_id: str,
    ) -> list[SemanticEntity]:
        ...

    def find_occupations_for_skill(
        self,
        skill_id: str,
    ) -> list[SemanticEntity]:
        ...
        
    def find_relation_type(
        self,
        occupation_id: str,
        skill_id: str,
    ) -> str | None:
        ...