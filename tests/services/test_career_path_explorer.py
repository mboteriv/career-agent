from career_agent.models.career_path import CareerPath
from career_agent.models.knowledge import Knowledge
from career_agent.models.occupation_match import OccupationMatch
from career_agent.models.occupation_skill_relation import (
    OccupationSkillRelation,
)
from career_agent.models.semantic_entity import SemanticEntity
from career_agent.models.skill_gap import SkillGap
from career_agent.repositories.sqlite_semantic_repository import (
    SQLiteSemanticRepository,
)
from career_agent.services.career_path_explorer import (
    CareerPathExplorer,
)


from career_agent.services.occupation_matcher import (
    OccupationMatcher,
)
from career_agent.services.skill_gap_analyzer import (
    SkillGapAnalyzer,
)
from career_agent.services.sqlite_database_builder import KnowledgeDatabaseBuilder


def test_explore_returns_matches_for_all_occupations(
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
                id="photoshop",
                preferred_label="Photoshop",
            ),
        ],
        occupations=[
            SemanticEntity(
                id="software-developer",
                preferred_label="Software developer",
            ),
            SemanticEntity(
                id="graphic-designer",
                preferred_label="Graphic designer",
            ),
        ],
        occupation_skill_relations=[
            OccupationSkillRelation(
                occupation_id="software-developer",
                skill_id="python",
                relation_type="essential",
            ),
            OccupationSkillRelation(
                occupation_id="graphic-designer",
                skill_id="photoshop",
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

    explorer = CareerPathExplorer(
        repository,
        matcher,
    )

    career_path = explorer.explore(
        candidate_skills=[
            "python",
        ],
    )

    assert career_path == CareerPath(
        occupations=[
            OccupationMatch(
                occupation=SemanticEntity(
                    id="software-developer",
                    preferred_label="Software developer",
                ),
                score=1.0,
                skill_gap=SkillGap(
                    total_essential=1,
                ),
            ),
            OccupationMatch(
                occupation=SemanticEntity(
                    id="graphic-designer",
                    preferred_label="Graphic designer",
                ),
                score=0.0,
                skill_gap=SkillGap(
                    missing_essential=[
                        SemanticEntity(
                            id="photoshop",
                            preferred_label="Photoshop",
                        ),
                    ],
                    total_essential=1,
                ),
            ),
        ],
    )
    
def test_explore_returns_limited_number_of_matches(
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
                id="photoshop",
                preferred_label="Photoshop",
            ),
        ],
        occupations=[
            SemanticEntity(
                id="software-developer",
                preferred_label="Software developer",
            ),
            SemanticEntity(
                id="graphic-designer",
                preferred_label="Graphic designer",
            ),
        ],
        occupation_skill_relations=[
            OccupationSkillRelation(
                occupation_id="software-developer",
                skill_id="python",
                relation_type="essential",
            ),
            OccupationSkillRelation(
                occupation_id="graphic-designer",
                skill_id="photoshop",
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

    explorer = CareerPathExplorer(
        repository,
        matcher,
    )

    career_path = explorer.explore(
        candidate_skills=[
            "python",
        ],
        limit=1,
    )

    assert career_path == CareerPath(
        occupations=[
            OccupationMatch(
                occupation=SemanticEntity(
                    id="software-developer",
                    preferred_label="Software developer",
                ),
                score=1.0,
                skill_gap=SkillGap(
                    total_essential=1,
                    total_optional=0,
                ),
            ),
        ],
    )