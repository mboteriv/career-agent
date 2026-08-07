from career_agent.models.knowledge import Knowledge
from career_agent.models.occupation_skill_relation import (
    OccupationSkillRelation,
)
from career_agent.models.recommendation_priority import RecommendationPriority
from career_agent.models.semantic_entity import SemanticEntity
from career_agent.models.skill_recommendation import (
    SkillRecommendation,
)
from career_agent.models.skill_recommendation_result import (
    SkillRecommendationResult,
)
from career_agent.repositories.sqlite_semantic_repository import (
    SQLiteSemanticRepository,
)
from career_agent.services.sqlite_database_builder import KnowledgeDatabaseBuilder

from career_agent.services.skill_gap_analyzer import (
    SkillGapAnalyzer,
)
from career_agent.services.skill_recommendation_engine import (
    SkillRecommendationEngine,
)


def test_recommend_skills_returns_missing_essential_skill(
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

    engine = SkillRecommendationEngine(
        analyzer,
    )

    result = engine.recommend_skills(
        occupation_id="software-developer",
        candidate_skills=[],
    )

    assert result == SkillRecommendationResult(
        recommendations=[
            SkillRecommendation(
                skill=SemanticEntity(
                    id="python",
                    preferred_label="Python",
                ),
                priority=RecommendationPriority.ESSENTIAL,
            ),
        ],
    )
    
def test_recommend_skills_returns_essential_and_optional_skills(
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

    engine = SkillRecommendationEngine(
        analyzer,
    )

    result = engine.recommend_skills(
        occupation_id="software-developer",
        candidate_skills=[],
    )

    assert result == SkillRecommendationResult(
        recommendations=[
            SkillRecommendation(
                skill=SemanticEntity(
                    id="python",
                    preferred_label="Python",
                ),
                priority=RecommendationPriority.ESSENTIAL,
            ),
            SkillRecommendation(
                skill=SemanticEntity(
                    id="git",
                    preferred_label="Git",
                ),
                priority=RecommendationPriority.OPTIONAL,
            ),
        ],
    )