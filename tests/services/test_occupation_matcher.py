from career_agent.models.knowledge import Knowledge
from career_agent.models.occupation_match import (
    OccupationMatch,
)
from career_agent.models.occupation_skill_relation import (
    OccupationSkillRelation,
)
from career_agent.models.semantic_entity import SemanticEntity
from career_agent.models.skill_gap import SkillGap
from career_agent.repositories.sqlite_semantic_repository import (
    SQLiteSemanticRepository,
)

from career_agent.services.occupation_matcher import (
    OccupationMatcher,
)
from career_agent.services.skill_gap_analyzer import (
    SkillGapAnalyzer,
)
from career_agent.services.sqlite_database_builder import KnowledgeDatabaseBuilder


def test_match_returns_full_score_when_candidate_has_all_skills(
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

    matcher = OccupationMatcher(
        analyzer,
    )

    match = matcher.match(
        occupation_id="software-developer",
        candidate_skills=[
            "python",
        ],
    )

    assert match == OccupationMatch(
        occupation=SemanticEntity(
            id="software-developer",
            preferred_label="Software developer",
        ),
        score=1.0,
        skill_gap=SkillGap(
            total_essential=1,
            total_optional=0,
        ),
    )
    
def test_match_returns_zero_score_when_missing_essential_skill(
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

    matcher = OccupationMatcher(
        analyzer,
    )

    match = matcher.match(
        occupation_id="software-developer",
        candidate_skills=[],
    )

    assert match == OccupationMatch(
        occupation=SemanticEntity(
            id="software-developer",
            preferred_label="Software developer",
        ),
        score=0.0,
        skill_gap=SkillGap(
            missing_essential=[
                SemanticEntity(
                    id="python",
                    preferred_label="Python",
                ),
            ],
            total_essential=1,
            total_optional=0,
        ),
    )
    
def test_match_returns_half_score_when_candidate_has_half_of_essential_skills(
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

    matcher = OccupationMatcher(
        analyzer,
    )

    match = matcher.match(
        occupation_id="software-developer",
        candidate_skills=[
            "python",
        ],
    )

    assert match == OccupationMatch(
        occupation=SemanticEntity(
            id="software-developer",
            preferred_label="Software developer",
        ),
        score=0.5,
        skill_gap=SkillGap(
            missing_essential=[
                SemanticEntity(
                    id="docker",
                    preferred_label="Docker",
                ),
            ],
            total_essential=2,
            total_optional=0,
        ),
    )