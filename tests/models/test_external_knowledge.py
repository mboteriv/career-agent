from career_agent.models.external_knowledge import (
    ExternalKnowledge,
)

from career_agent.models.semantic_entity import (
    SemanticEntity,
)


def test_create_empty_external_knowledge():

    knowledge = ExternalKnowledge()

    assert knowledge.skills == []

    assert knowledge.occupations == []


def test_create_external_knowledge():

    python = SemanticEntity(
        id="python",
        preferred_label="Python",
    )

    translator = SemanticEntity(
        id="translator",
        preferred_label="Translator",
    )

    knowledge = ExternalKnowledge(
        skills=[
            python,
        ],
        occupations=[
            translator,
        ],
    )

    assert knowledge.skills == [
        python,
    ]

    assert knowledge.occupations == [
        translator,
    ]