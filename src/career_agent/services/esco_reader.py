import csv

from pathlib import Path

from career_agent.models.external_knowledge import (
    ExternalKnowledge,
)
from career_agent.models.semantic_entity import (
    SemanticEntity,
)
from career_agent.models.occupation_skill_relation import (
    OccupationSkillRelation,
)

class ESCOReader:
    
    def __init__(
        self,
        skills_path: Path,
        occupations_path: Path,
        occupation_skill_relations_path: Path,
    ):
        self._skills_path = skills_path
        self._occupations_path = occupations_path
        self._occupation_skill_relations_path = (
            occupation_skill_relations_path
        )

    def read(
        self,
    ) -> ExternalKnowledge:

        skills = []
        occupations = []
        occupation_skill_relations = []

        with self._skills_path.open(
            newline="",
            encoding="utf-8",
        ) as file:

            reader = csv.DictReader(file)
            
            aliases = []

            for row in reader:
                
                if row["altLabels"]:
                    aliases = [
                        alias.strip()
                        for alias in row["altLabels"].splitlines()
                        if alias.strip()
                    ]
                            
                    skills.append(
                        SemanticEntity(
                            id=row["preferredLabel"].lower(),
                            preferred_label=row["preferredLabel"],
                            description=row["definition"] or None,
                            aliases=aliases,
                        )
                    )
        with self._occupations_path.open(
            newline="",
            encoding="utf-8",
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:

                aliases = []

                if row["altLabels"]:
                    aliases = [
                        alias.strip()
                        for alias in row["altLabels"].splitlines()
                        if alias.strip()
                    ]

                occupations.append(
                    SemanticEntity(
                        id=row["preferredLabel"].lower(),
                        preferred_label=row["preferredLabel"],
                        description=row["definition"] or None,
                        aliases=aliases,
                    )
                )
        with self._occupation_skill_relations_path.open(
            newline="",
            encoding="utf-8",
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:

                occupation_skill_relations.append(
                    OccupationSkillRelation(
                        occupation_id=row["occupationUri"],
                        skill_id=row["skillUri"],
                        relation_type=row["relationType"],
                    )
                )

        return ExternalKnowledge(
            skills=skills,
            occupations=occupations,
            occupation_skill_relations=occupation_skill_relations,
        )
        
def test_read_imports_occupation_skill_relations():
    
    knowledge = reader.read()

    assert knowledge.occupation_skill_relations == [
        OccupationSkillRelation(
            occupation_id="occupation1",
            skill_id="skill1",
            relation_type="essential",
        ),
    ]