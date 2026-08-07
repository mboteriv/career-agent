from career_agent.models.knowledge import KnowledgeCompiler
from career_agent.services.esco_reader import (
    ESCOReader,
)
from career_agent.models.semantic_entity import (
    SemanticEntity,
)
from pathlib import Path



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


def test_compile_imported_skills():

    reader = ESCOReader(
        TEST_SKILLS,
        TEST_OCCUPATIONS,
        TEST_OCCUPATION_SKILL_RELATIONS,
    )

    external = reader.read()

    compiler = KnowledgeCompiler()

    knowledge = compiler.compile(
        external,
    )

    assert len(
        knowledge.skills,
    ) == 2