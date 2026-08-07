import sqlite3

from pathlib import Path

from career_agent.models.knowledge import Knowledge
from career_agent.repositories.semantic_repository import (
    SemanticRepository,
)


class KnowledgeDatabaseBuilder:

    def build(
        self,
        knowledge: Knowledge,
        database_path: Path,
    ) -> None:

        connection = sqlite3.connect(
            database_path,
        )
        
             
        connection.execute(
            """
            CREATE TABLE skill(

                id TEXT PRIMARY KEY,

                preferred_label TEXT NOT NULL,

                description TEXT
            )
            """
        )
        
        connection.execute(
            """
            CREATE TABLE skill_alias(

                skill_id TEXT NOT NULL,

                alias TEXT NOT NULL,

                normalized_alias TEXT NOT NULL,

                PRIMARY KEY(
                    skill_id,
                    alias
                ),

                FOREIGN KEY(skill_id)
                REFERENCES skill(id)
            )
            """
        )
        
        connection.execute(
            """
            CREATE TABLE occupation(
        
                id TEXT PRIMARY KEY,
        
                preferred_label TEXT NOT NULL,

                description TEXT
            )
            """
        )
        
        connection.execute(
            """
            CREATE TABLE occupation_skill_relation(

                occupation_id TEXT NOT NULL,

                skill_id TEXT NOT NULL,

                relation_type TEXT NOT NULL
            )
            """
        )
                
        for skill in knowledge.skills:
        
            connection.execute(
                """
                INSERT INTO skill(
                    id,
                    preferred_label,
                    description
                )
                VALUES (?, ?, ?)
                    """,
                (
                    skill.id,
                    skill.preferred_label,
                    skill.description,
                ),
            )
            
        for skill in knowledge.skills:

            for alias in skill.aliases:

                connection.execute(
                    """
                    INSERT INTO skill_alias(
                        skill_id,
                        alias,
                        normalized_alias
                    )
                    VALUES (?, ?, ?)
                    """,
                    (
                        skill.id,
                        alias,
                        alias.lower(),
                    ),
                )
        for occupation in knowledge.occupations:

            connection.execute(
                """
                INSERT INTO occupation(
                    id,
                    preferred_label,
                    description
                )
                VALUES (?, ?, ?)
                """,
                (
                    occupation.id,
                    occupation.preferred_label,
                    occupation.description,
                ),
            )
        
        for relation in knowledge.occupation_skill_relations:

            connection.execute(
                """
                INSERT INTO occupation_skill_relation(
                    occupation_id,
                    skill_id,
                    relation_type
                )
                VALUES (?, ?, ?)
                """,
                (
                    relation.occupation_id,
                    relation.skill_id,
                    relation.relation_type,
                ),
            )

        connection.commit()
        
        connection.close()
        
class SQLiteSemanticRepository(
    SemanticRepository,
):

    def __init__(
        self,
        database_path: Path,
    ):
        self._database_path = database_path
        
    def __init__(self, database_path: Path):
        self._database_path = database_path

        with sqlite3.connect(
            self._database_path,
        ) as connection:

            row = connection.execute(
                """
                SELECT
                    id,
                    preferred_label
                FROM skill
                WHERE preferred_label = ?
                """,
                (
                    label,
                ),
            ).fetchone()

        if row is None:
            return None

        return SemanticEntity(
            id=row[0],
            preferred_label=row[1],
        )
    
    
        
