
import sqlite3

from career_agent.models.knowledge import Knowledge
from career_agent.models.occupation_skill_relation import OccupationSkillRelation
from career_agent.models.semantic_entity import SemanticEntity
from career_agent.repositories.sqlite_semantic_repository import SQLiteSemanticRepository
from career_agent.services.sqlite_database_builder import KnowledgeDatabaseBuilder


def test_find_skill_by_label_returns_skill(
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
        

    entity = repository.find_skill_by_label(
        "Python",
    )
    with sqlite3.connect(database) as connection:
        rows = connection.execute(
            "SELECT id, preferred_label FROM skill"
        ).fetchall()

    print(rows)
    
    assert entity == SemanticEntity(
        id="python",
        preferred_label="Python",
    )

def test_find_skill_by_label_returns_none_when_skill_does_not_exist(
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
        "Rust",
    )

    assert entity is None

def test_build_creates_database_file(
    tmp_path,
):

    database = tmp_path / "career_agent.db"

    builder = KnowledgeDatabaseBuilder()

    builder.build(
        Knowledge(),
        database,
    )

    assert database.exists()
    

def test_build_creates_skill_table(
    tmp_path,
):

    database = tmp_path / "career_agent.db"

    builder = KnowledgeDatabaseBuilder()

    builder.build(
        Knowledge(),
        database,
    )

    connection = sqlite3.connect(
        database,
    )

    cursor = connection.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        """
    )

    tables = {
        row[0]
        for row in cursor.fetchall()
    }

    connection.close()

    assert "skill" in tables
    
def test_build_inserts_skills(
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

    with sqlite3.connect(database) as connection:

        rows = connection.execute(
            """
            SELECT id, preferred_label
            FROM skill
            """
        ).fetchall()

    assert rows == [
        (
            "python",
            "Python",
        ),
    ]
    
def test_build_inserts_multiple_skills(
    tmp_path,
):

    database = tmp_path / "career_agent.db"

    knowledge = Knowledge(
        skills=[
            SemanticEntity(
                id="python",
                preferred_label="Python",
            ),
            SemanticEntity(
                id="docker",
                preferred_label="Docker",
            ),
            SemanticEntity(
                id="git",
                preferred_label="Git",
            ),
        ],
    )

    builder = KnowledgeDatabaseBuilder()

    builder.build(
        knowledge,
        database,
    )

    with sqlite3.connect(database) as connection:

        rows = connection.execute(
            """
            SELECT
                id,
                preferred_label
            FROM skill
            ORDER BY id
            """
        ).fetchall()

    assert rows == [
        (
            "docker",
            "Docker",
        ),
        (
            "git",
            "Git",
        ),
        (
            "python",
            "Python",
        ),
    ]
    
def test_build_creates_skill_alias_table(
    tmp_path,
):

    database = tmp_path / "career_agent.db"

    builder = KnowledgeDatabaseBuilder()

    builder.build(
        Knowledge(),
        database,
    )

    with sqlite3.connect(database) as connection:

        tables = {
            row[0]
            for row in connection.execute(
                """
                SELECT name
                FROM sqlite_master
                WHERE type='table'
                """
            ).fetchall()
        }

    assert "skill_alias" in tables
    
def test_build_inserts_skill_aliases(
    tmp_path,
):

    database = tmp_path / "career_agent.db"

    knowledge = Knowledge(
        skills=[
            SemanticEntity(
                id="python",
                preferred_label="Python",
                aliases=[
                    "Python 3",
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

    with sqlite3.connect(database) as connection:

        rows = connection.execute(
            """
            SELECT
                skill_id,
                alias
            FROM skill_alias
            ORDER BY alias
            """
        ).fetchall()

    assert rows == [
        (
            "python",
            "Python 3",
        ),
        (
            "python",
            "Python Programming",
        ),
    ]
    
def test_build_inserts_occupations(
    tmp_path,
):

    database = tmp_path / "career_agent.db"

    knowledge = Knowledge(
        occupations=[
            SemanticEntity(
                id="software-developer",
                preferred_label="Software developer",
                description="Develops software.",
            ),
        ],
    )

    builder = KnowledgeDatabaseBuilder()

    builder.build(
        knowledge,
        database,
    )

    with sqlite3.connect(database) as connection:

        rows = connection.execute(
            """
            SELECT
                id,
                preferred_label,
                description
            FROM occupation
            """
        ).fetchall()

    assert rows == [
        (
            "software-developer",
            "Software developer",
            "Develops software.",
        ),
    ]
    
def test_build_inserts_occupation_skill_relations(
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

    with sqlite3.connect(database) as connection:

        rows = connection.execute(
            """
            SELECT
                occupation_id,
                skill_id,
                relation_type
            FROM occupation_skill_relation
            """
        ).fetchall()

    assert rows == [
        (
            "software-developer",
            "python",
            "essential",
        ),
    ]