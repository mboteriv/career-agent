from career_agent.models.knowledge import (
    Knowledge,
    KnowledgeCompiler,
)
from career_agent.models.semantic_entity import (
    SemanticEntity,
)
from career_agent.models.external_knowledge import (
    ExternalKnowledge,
)



def test_create_empty_knowledge():

    knowledge = Knowledge()

    assert knowledge.skills == []

    assert knowledge.occupations == []
    
def test_create_knowledge():

    python = SemanticEntity(
        id="python",
        preferred_label="Python",
    )

    translator = SemanticEntity(
        id="translator",
        preferred_label="Translator",
    )

    knowledge = Knowledge(
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
    

def test_compile_returns_knowledge():

    compiler = KnowledgeCompiler()

    external = ExternalKnowledge(
        skills=[
            SemanticEntity(
                id="python",
                preferred_label="Python",
            ),
        ],
    )

    knowledge = compiler.compile(
        external,
    )

    assert isinstance(
        knowledge,
        Knowledge,
    )

    assert knowledge.skills == external.skills
    
def test_compile_returns_empty_knowledge():

    compiler = KnowledgeCompiler()

    knowledge = compiler.compile(
        ExternalKnowledge(),
    )

    assert knowledge == Knowledge()