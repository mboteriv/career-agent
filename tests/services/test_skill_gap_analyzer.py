import sqlite3

from career_agent.models.knowledge import Knowledge
from career_agent.models.occupation_skill_relation import (
    OccupationSkillRelation,
)
from career_agent.models.semantic_entity import SemanticEntity
from career_agent.models.skill_gap import SkillGap
from career_agent.repositories.sqlite_semantic_repository import (
    SQLiteSemanticRepository,
)

from career_agent.services.skill_gap_analyzer import (
    SkillGapAnalyzer,
)
from career_agent.services.sqlite_database_builder import KnowledgeDatabaseBuilder


def test_analyze_returns_empty_gap_when_candidate_has_all_skills(
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

    analyzer = SkillGapAnalyzer(
        repository,
    )

    gap = analyzer.analyze(
        occupation_id="software-developer",
        candidate_skills=[
            "python",
        ],
    )

    assert gap == SkillGap(
        total_essential=1,
        total_optional=0,
    )
    
def test_analyze_returns_missing_essential_skill(
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

    analyzer = SkillGapAnalyzer(
        repository,
    )

    gap = analyzer.analyze(
        occupation_id="software-developer",
        candidate_skills=[],
    )

    assert gap == SkillGap(
        missing_essential=[
            SemanticEntity(
                id="python",
                preferred_label="Python",
            ),
        ],
        total_essential=1,
        total_optional=0,
    )
    
def test_analyze_returns_missing_optional_skill(
    tmp_path,
):

    database = tmp_path / "career_agent.db"

    knowledge = Knowledge(
        skills=[
            SemanticEntity(
                id="git",
                preferred_label="Git",
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
                skill_id="git",
                relation_type="optional",
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

    analyzer = SkillGapAnalyzer(
        repository,
    )

    gap = analyzer.analyze(
        occupation_id="software-developer",
        candidate_skills=[],
    )

    assert gap == SkillGap(
        missing_optional=[
            SemanticEntity(
                id="git",
                preferred_label="Git",
            ),
        ],
        total_essential=0,
        total_optional=1,
    )
    
def test_analyze_returns_complete_skill_gap(
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
            OccupationSkillRelation(
                occupation_id="software-developer",
                skill_id="docker",
                relation_type="essential",
            ),
            OccupationSkillRelation(
                occupation_id="software-developer",
                skill_id="git",
                relation_type="optional",
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

    analyzer = SkillGapAnalyzer(
        repository,
    )

    gap = analyzer.analyze(
        occupation_id="software-developer",
        candidate_skills=[
            "python",
        ],
    )

    assert gap == SkillGap(
        missing_essential=[
            SemanticEntity(
                id="docker",
                preferred_label="Docker",
            ),
        ],
        missing_optional=[
            SemanticEntity(
                id="git",
                preferred_label="Git",
            ),
        ],
        total_essential=2,
        total_optional=1,
    )