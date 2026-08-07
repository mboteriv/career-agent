import sqlite3
from pathlib import Path

from career_agent.models.semantic_entity import SemanticEntity
from career_agent.models.occupation_skill_relation import OccupationSkillRelation
from career_agent.repositories.semantic_repository import (
    SemanticRepository,
)


class SQLiteSemanticRepository(
    SemanticRepository,
):

    def __init__(
        self,
        database_path: Path,
    ):
        self._database_path = database_path
        
    
    def find_skill_by_label(
        self,
        label: str,
    ) -> SemanticEntity | None:

        with sqlite3.connect(self._database_path) as connection:

            row = connection.execute(
                """
                SELECT
                    id,
                    preferred_label,
                    description
                FROM skill
                WHERE preferred_label = ?
                """,
                (label,),
            ).fetchone()

        if row is None:
            return None

        return SemanticEntity(
            id=row[0],
            preferred_label=row[1],
            description=row[2],
        )
        
    def find_skill_by_alias(
        self,
        alias: str,
    ) -> SemanticEntity | None:

        with sqlite3.connect(
            self._database_path,
        ) as connection:

            row = connection.execute(
                """
                SELECT
                    s.id,
                    s.preferred_label,
                    s.description
                FROM skill s
                JOIN skill_alias a
                    ON a.skill_id = s.id
                WHERE a.alias = ?
                """,
                (alias,),
            ).fetchone()

        if row is None:
            return None

        return SemanticEntity(
            id=row[0],
            preferred_label=row[1],
            description=row[2],
        )
        
    def find_skills_for_occupation(
            self,
            occupation_id: str,
        ) -> list[SemanticEntity]:
    
            with sqlite3.connect(
                self._database_path,
            ) as connection:
    
                rows = connection.execute(
                    """
                    SELECT
                        s.id,
                        s.preferred_label,
                        s.description
                    FROM skill s
                    JOIN occupation_skill_relation r
                        ON r.skill_id = s.id
                    WHERE r.occupation_id = ?
                    ORDER BY s.preferred_label
                    """,
                (occupation_id,),
            ).fetchall()
    
            return [
                SemanticEntity(
                    id=row[0],
                    preferred_label=row[1],
                    description=row[2],
                )
                for row in rows
            ]
            
    def find_occupations_for_skill(
        self,
        skill_id: str,
    ) -> list[SemanticEntity]:

        with sqlite3.connect(
            self._database_path,
        ) as connection:

            rows = connection.execute(
                """
                SELECT
                    o.id,
                    o.preferred_label,
                    o.description
                FROM occupation o
                JOIN occupation_skill_relation r
                    ON r.occupation_id = o.id
                WHERE r.skill_id = ?
                ORDER BY o.preferred_label
                """,
                (skill_id,),
            ).fetchall()

        return [
            SemanticEntity(
                id=row[0],
                preferred_label=row[1],
                description=row[2],
            )
            for row in rows
        ]
    
    def find_relation_type(
        self,
        occupation_id: str,
        skill_id: str,
    ) -> str | None:

        with sqlite3.connect(
            self._database_path,
        ) as connection:

            row = connection.execute(
                """
                SELECT
                    relation_type
                FROM occupation_skill_relation
                WHERE occupation_id = ?
                AND skill_id = ?
                """,
                (
                    occupation_id,
                    skill_id,
                ),
            ).fetchone()

        if row is None:
            return None

        return row[0]