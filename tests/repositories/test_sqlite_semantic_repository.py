from career_agent.models.knowledge import Knowledge
from career_agent.models.semantic_entity import SemanticEntity
from career_agent.models.skill_dependency import SkillDependency
from career_agent.repositories.sqlite_semantic_repository import (
    SQLiteSemanticRepository,
)
from career_agent.services.sqlite_database_builder import (
    KnowledgeDatabaseBuilder,
)
from career_agent.models.occupation_skill_relation import (
    OccupationSkillRelation,
)

def test_find_skill_by_label_returns_none(
    tmp_path,
):

    database = tmp_path / "career_agent.db"

    builder = KnowledgeDatabaseBuilder()

    builder.build(
        Knowledge(),
        database,
    )

    repository = SQLiteSemanticRepository(
        database,
    )

    entity = repository.find_skill_by_label(
        "Python",
    )

    assert entity is None
    
def test_find_skill_by_alias_returns_skill(
    tmp_path,
):

    database = tmp_path / "career_agent.db"

    knowledge = Knowledge(
        skills=[
            SemanticEntity(
                id="python",
                preferred_label="Python",
                aliases=[
                    "Python Programming",
                ],
            ),
        ],
    )

    builder = KnowledgeDatabaseBuilder()

    builder.build(
        knowledge,
        database,
    )

    repository = SQLiteSemanticRepository(
        database,
    )

    entity = repository.find_skill_by_alias(
        "Python Programming",
    )

    assert entity == SemanticEntity(
        id="python",
        preferred_label="Python",
    )
    
def test_find_skill_by_alias_returns_none(
    tmp_path,
):

    database = tmp_path / "career_agent.db"

    knowledge = Knowledge(
        skills=[
            SemanticEntity(
                id="python",
                preferred_label="Python",
                aliases=[
                    "Python Programming",
                ],
            ),
        ],
    )

    builder = KnowledgeDatabaseBuilder()

    builder.build(
        knowledge,
        database,
    )

    repository = SQLiteSemanticRepository(
        database,
    )

    entity = repository.find_skill_by_alias(
        "Rust",
    )

    assert entity is None
    
def test_find_skill_by_label_returns_description(
    tmp_path,
):

    database = tmp_path / "career_agent.db"

    knowledge = Knowledge(
        skills=[
            SemanticEntity(
                id="python",
                preferred_label="Python",
                description="Programming language",
            ),
        ],
    )

    builder = KnowledgeDatabaseBuilder()

    builder.build(
        knowledge,
        database,
    )

    repository = SQLiteSemanticRepository(
        database,
    )

    entity = repository.find_skill_by_label(
        "Python",
    )

    assert entity.description == "Programming language"
    
def test_find_skills_for_occupation_returns_skills(
    tmp_path,
):

    database = tmp_path / "career_agent.db"

    knowledge = Knowledge(
        skills=[
            SemanticEntity(
                id="python",
                preferred_label="Python",
            ),
        ],
        occupations=[
            SemanticEntity(
                id="software-developer",
                preferred_label="Software developer",
            ),
        ],
        occupation_skill_relations=[
            OccupationSkillRelation(
                occupation_id="software-developer",
                skill_id="python",
                relation_type="essential",
            ),
        ],
    )

    builder = KnowledgeDatabaseBuilder()

    builder.build(
        knowledge,
        database,
    )

    repository = SQLiteSemanticRepository(
        database,
    )

    skills = repository.find_skills_for_occupation(
        "software-developer",
    )

    assert skills == [
        SemanticEntity(
            id="python",
            preferred_label="Python",
        ),
    ]
    
def test_find_skills_for_unknown_occupation_returns_empty_list(
    tmp_path,
):

    database = tmp_path / "career_agent.db"

    builder = KnowledgeDatabaseBuilder()

    builder.build(
        Knowledge(),
        database,
    )

    repository = SQLiteSemanticRepository(
        database,
    )

    skills = repository.find_skills_for_occupation(
        "unknown",
    )

    assert skills == []
    
def test_find_occupations_for_skill_returns_occupations(
    tmp_path,
):

    database = tmp_path / "career_agent.db"

    knowledge = Knowledge(
        skills=[
            SemanticEntity(
                id="python",
                preferred_label="Python",
            ),
        ],
        occupations=[
            SemanticEntity(
                id="software-developer",
                preferred_label="Software developer",
                description="Develops software.",
            ),
        ],
        occupation_skill_relations=[
            OccupationSkillRelation(
                occupation_id="software-developer",
                skill_id="python",
                relation_type="essential",
            ),
        ],
    )

    builder = KnowledgeDatabaseBuilder()

    builder.build(
        knowledge,
        database,
    )

    repository = SQLiteSemanticRepository(
        database,
    )

    occupations = repository.find_occupations_for_skill(
        "python",
    )

    assert occupations == [
        SemanticEntity(
            id="software-developer",
            preferred_label="Software developer",
            description="Develops software.",
        ),
    ]
    
def test_find_occupations_for_unknown_skill_returns_empty_list(
    tmp_path,
):

    database = tmp_path / "career_agent.db"

    builder = KnowledgeDatabaseBuilder()

    builder.build(
        Knowledge(),
        database,
    )

    repository = SQLiteSemanticRepository(
        database,
    )

    occupations = repository.find_occupations_for_skill(
        "unknown",
    )

    assert occupations == []
    
def test_find_relation_type_returns_relation_type(
    tmp_path,
):

    database = tmp_path / "career_agent.db"

    knowledge = Knowledge(
        occupation_skill_relations=[
            OccupationSkillRelation(
                occupation_id="software-developer",
                skill_id="python",
                relation_type="essential",
            ),
        ],
    )

    builder = KnowledgeDatabaseBuilder()

    builder.build(
        knowledge,
        database,
    )

    repository = SQLiteSemanticRepository(
        database,
    )

    relation_type = repository.find_relation_type(
        occupation_id="software-developer",
        skill_id="python",
    )

    assert relation_type == "essential"
    
def test_find_relation_type_returns_none_when_relation_does_not_exist(
    tmp_path,
):

    database = tmp_path / "career_agent.db"

    builder = KnowledgeDatabaseBuilder()

    builder.build(
        Knowledge(),
        database,
    )

    repository = SQLiteSemanticRepository(
        database,
    )

    relation_type = repository.find_relation_type(
        occupation_id="software-developer",
        skill_id="python",
    )

    assert relation_type is None
    
def test_find_prerequisites_returns_prerequisite_skills(
    tmp_path,
):

    database = tmp_path / "career_agent.db"

    knowledge = Knowledge(
        skills=[
            SemanticEntity(
                id="git",
                preferred_label="Git",
            ),
            SemanticEntity(
                id="docker",
                preferred_label="Docker",
            ),
        ],
        skill_dependencies=[
            SkillDependency(
                prerequisite_skill_id="git",
                dependent_skill_id="docker",
            ),
        ],
    )

    builder = KnowledgeDatabaseBuilder()

    builder.build(
        knowledge,
        database,
    )

    repository = SQLiteSemanticRepository(
        database,
    )

    assert repository.find_prerequisites(
        "docker",
    ) == [
        SemanticEntity(
            id="git",
            preferred_label="Git",
        ),
    ]
    
def test_find_prerequisites_returns_empty_list_when_skill_has_no_prerequisites(
    tmp_path,
):

    database = tmp_path / "career_agent.db"

    knowledge = Knowledge(
        skills=[
            SemanticEntity(
                id="python",
                preferred_label="Python",
            ),
        ],
    )

    builder = KnowledgeDatabaseBuilder()

    builder.build(
        knowledge,
        database,
    )

    repository = SQLiteSemanticRepository(
        database,
    )

    assert repository.find_prerequisites(
        "python",
    ) == []