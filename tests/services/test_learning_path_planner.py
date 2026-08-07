


from career_agent.models.knowledge import Knowledge
from career_agent.models.learning_path import LearningPath
from career_agent.models.occupation_skill_relation import OccupationSkillRelation
from career_agent.models.recommendation_priority import RecommendationPriority
from career_agent.models.semantic_entity import SemanticEntity
from career_agent.models.skill_dependency import SkillDependency
from career_agent.models.skill_recommendation import SkillRecommendation
from career_agent.repositories.sqlite_semantic_repository import SQLiteSemanticRepository
from career_agent.services.learning_path_planner import LearningPathPlanner
from career_agent.services.skill_gap_analyzer import SkillGapAnalyzer
from career_agent.services.skill_recommendation_engine import SkillRecommendationEngine
from career_agent.services.sqlite_database_builder import KnowledgeDatabaseBuilder


def test_plan_returns_learning_path(
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

    planner = LearningPathPlanner(
        engine,
        repository,
    )

    learning_path = planner.plan(
        occupation_id="software-developer",
        candidate_skills=[],
    )
    print(learning_path.model_dump())

    assert learning_path == LearningPath(
        steps=[
            SkillRecommendation(
                skill=SemanticEntity(
                    id="python",
                    preferred_label="Python",
                ),
                priority=RecommendationPriority.ESSENTIAL,
            ),
        ],
    )
    
def test_plan_includes_prerequisites_before_recommended_skills(
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
        occupations=[
            SemanticEntity(
                id="software-developer",
                preferred_label="Software developer",
            ),
        ],
        occupation_skill_relations=[
            OccupationSkillRelation(
                occupation_id="software-developer",
                skill_id="docker",
                relation_type="essential",
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

    analyzer = SkillGapAnalyzer(
        repository,
    )

    engine = SkillRecommendationEngine(
        analyzer,
    )

    planner = LearningPathPlanner(
        engine,
        repository,
    )

    learning_path = planner.plan(
        occupation_id="software-developer",
        candidate_skills=[],
    )

    assert learning_path == LearningPath(
        steps=[
            SkillRecommendation(
                skill=SemanticEntity(
                    id="git",
                    preferred_label="Git",
                ),
                priority=RecommendationPriority.ESSENTIAL,
            ),
            SkillRecommendation(
                skill=SemanticEntity(
                    id="docker",
                    preferred_label="Docker",
                ),
                priority=RecommendationPriority.ESSENTIAL,
            ),
        ],
    )
    
def test_plan_includes_transitive_prerequisites(
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
            SemanticEntity(
                id="kubernetes",
                preferred_label="Kubernetes",
            ),
        ],
        occupations=[
            SemanticEntity(
                id="platform-engineer",
                preferred_label="Platform engineer",
            ),
        ],
        occupation_skill_relations=[
            OccupationSkillRelation(
                occupation_id="platform-engineer",
                skill_id="kubernetes",
                relation_type="essential",
            ),
        ],
        skill_dependencies=[
            SkillDependency(
                prerequisite_skill_id="git",
                dependent_skill_id="docker",
            ),
            SkillDependency(
                prerequisite_skill_id="docker",
                dependent_skill_id="kubernetes",
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

    planner = LearningPathPlanner(
        engine,
        repository,
    )

    learning_path = planner.plan(
        occupation_id="platform-engineer",
        candidate_skills=[],
    )

    assert learning_path == LearningPath(
        steps=[
            SkillRecommendation(
                skill=SemanticEntity(
                    id="git",
                    preferred_label="Git",
                ),
                priority=RecommendationPriority.ESSENTIAL,
            ),
            SkillRecommendation(
                skill=SemanticEntity(
                    id="docker",
                    preferred_label="Docker",
                ),
                priority=RecommendationPriority.ESSENTIAL,
            ),
            SkillRecommendation(
                skill=SemanticEntity(
                    id="kubernetes",
                    preferred_label="Kubernetes",
                ),
                priority=RecommendationPriority.ESSENTIAL,
            ),
        ],
    )
    
def test_plan_does_not_duplicate_prerequisites(
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
            SemanticEntity(
                id="linux",
                preferred_label="Linux",
            ),
        ],
        occupations=[
            SemanticEntity(
                id="devops-engineer",
                preferred_label="DevOps engineer",
            ),
        ],
        occupation_skill_relations=[
            OccupationSkillRelation(
                occupation_id="devops-engineer",
                skill_id="docker",
                relation_type="essential",
            ),
            OccupationSkillRelation(
                occupation_id="devops-engineer",
                skill_id="linux",
                relation_type="essential",
            ),
        ],
        skill_dependencies=[
            SkillDependency(
                prerequisite_skill_id="git",
                dependent_skill_id="docker",
            ),
            SkillDependency(
                prerequisite_skill_id="git",
                dependent_skill_id="linux",
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

    planner = LearningPathPlanner(
        engine,
        repository,
    )

    learning_path = planner.plan(
        occupation_id="devops-engineer",
        candidate_skills=[],
    )

    assert learning_path == LearningPath(
        steps=[
            SkillRecommendation(
                skill=SemanticEntity(
                    id="git",
                    preferred_label="Git",
                ),
                priority=RecommendationPriority.ESSENTIAL,
            ),
            SkillRecommendation(
                skill=SemanticEntity(
                    id="docker",
                    preferred_label="Docker",
                ),
                priority=RecommendationPriority.ESSENTIAL,
            ),
            SkillRecommendation(
                skill=SemanticEntity(
                    id="linux",
                    preferred_label="Linux",
                ),
                priority=RecommendationPriority.ESSENTIAL,
            ),
        ],
    )