from career_agent.models.semantic_entity import (
    SemanticEntity,
)


def test_create_semantic_entity():

    entity = SemanticEntity(
        id="python",
        preferred_label="Python",
    )

    assert entity.id == "python"
    assert entity.preferred_label == "Python"
    assert entity.aliases == []
    assert entity.external_ids == {}
    
def test_create_semantic_entity_with_aliases():

    entity = SemanticEntity(
        id="python",
        preferred_label="Python",
        aliases=[
            "Python 3",
            "Python Programming",
        ],
        external_ids={
            "ESCO": "skill-123",
        },
    )

    assert entity.aliases == [
        "Python 3",
        "Python Programming",
    ]

    assert entity.external_ids == {
        "ESCO": "skill-123",
    }