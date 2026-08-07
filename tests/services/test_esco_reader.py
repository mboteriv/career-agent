import csv

from pathlib import Path

from career_agent.models.external_knowledge import (
    ExternalKnowledge,
)
from career_agent.models.knowledge import KnowledgeCompiler
from career_agent.models.semantic_entity import (
    SemanticEntity,
)
from career_agent.services.esco_reader import (
    ESCOReader,
)

TEST_SKILLS = (
    Path(__file__).parent.parent
    / "data"
    / "skills.csv"
)

TEST_OCCUPATIONS = (
    Path(__file__).parent.parent
    / "data"
    / "occupations.csv"
)

TEST_OCCUPATION_SKILL_RELATIONS = (
    Path(__file__).parent.parent
    / "data"
    / "occupation_skill_relations.csv"
)

def test_read_returns_external_knowledge():

    reader = ESCOReader(
        TEST_SKILLS,
        TEST_OCCUPATIONS,
        TEST_OCCUPATION_SKILL_RELATIONS,
    )

    knowledge = reader.read()

    assert isinstance(
        knowledge,
        ExternalKnowledge,
    )
    
def test_read_imports_skills():
  
    reader = ESCOReader(
        TEST_SKILLS,
        TEST_OCCUPATIONS,
        TEST_OCCUPATION_SKILL_RELATIONS,
    )
    
    knowledge = reader.read()

    assert len(
        knowledge.skills,
    ) > 0

def test_read_imports_skill_aliases():

    reader = ESCOReader(
        TEST_SKILLS,
        TEST_OCCUPATIONS,
        TEST_OCCUPATION_SKILL_RELATIONS,
    )

    knowledge = reader.read()

    assert knowledge.skills[0].aliases == [
        "Python Programming",
        "Python 3",
    ]
    
def test_read_imports_skill_aliases():

    reader = ESCOReader(
        TEST_SKILLS,
        TEST_OCCUPATIONS,
        TEST_OCCUPATION_SKILL_RELATIONS,
    )

    knowledge = reader.read()

    assert knowledge.skills[0].aliases == [
        "Python Programming",
        "Python 3",
    ]
    
def test_read_imports_skill_description():

    reader = ESCOReader(
        TEST_SKILLS,
        TEST_OCCUPATIONS,
        TEST_OCCUPATION_SKILL_RELATIONS,
    )

    knowledge = reader.read()

    assert knowledge.skills[0].description == (
        "Programming language"
    )
    
def test_read_imports_occupations():

    reader = ESCOReader(
        TEST_SKILLS,
        TEST_OCCUPATIONS,
        TEST_OCCUPATION_SKILL_RELATIONS,
    )
    

    knowledge = reader.read()

    assert knowledge.occupations == [
        SemanticEntity(
            id="software developer",
            preferred_label="Software developer",
            description="Develops and maintains software applications.",
            aliases=[
                "Software engineer",
                "Software programmer",
            ],
        ),
    ]