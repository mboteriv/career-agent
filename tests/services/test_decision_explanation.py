from career_agent.models.decision_explanation import DecisionExplanation
from career_agent.models.knowledge import Knowledge
from career_agent.models.learning_path import LearningPath
from career_agent.models.learning_path_explanation import LearningPathExplanation
from career_agent.models.occupation_skill_relation import OccupationSkillRelation
from career_agent.models.recommendation_explanation import RecommendationExplanation
from career_agent.models.recommendation_priority import RecommendationPriority
from career_agent.models.semantic_entity import SemanticEntity
from career_agent.models.skill_dependency import SkillDependency
from career_agent.models.skill_recommendation import SkillRecommendation
from career_agent.services.decision_explainer import DecisionExplainer
from career_agent.services.learning_path_explainer import LearningPathExplainer
from career_agent.services.learning_path_planner import LearningPathPlanner
from career_agent.services.occupation_matcher import OccupationMatcher
from career_agent.services.recommendation_explainer import RecommendationExplainer
from career_agent.services.skill_gap_analyzer import SkillGapAnalyzer
from career_agent.services.skill_recommendation_engine import SkillRecommendationEngine
from career_agent.services.sqlite_database_builder import (
    KnowledgeDatabaseBuilder,
)

from career_agent.repositories.sqlite_semantic_repository import (
    SQLiteSemanticRepository,
)


def test_match_can_be_explained(
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
    print(
        "ABSTRACT:",
        SQLiteSemanticRepository.__abstractmethods__,
    )

    print(
        "MODULE:",
        SQLiteSemanticRepository.__module__,
    )

    import inspect

    print(
        "FILE:",
        inspect.getfile(SQLiteSemanticRepository),
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

    explainer = DecisionExplainer()

    explanation = explainer.explain(
        match,
    )

    assert explanation == DecisionExplanation(
        summary=(
            "Software developer is a partial match (50%)."
        ),
        reasons=[
            "You are missing the essential skill: Docker.",
        ],
    )
    
def test_full_match_can_be_explained(
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
        candidate_skills=["python"],
    )

    explainer = DecisionExplainer()

    explanation = explainer.explain(
        match,
    )

    assert explanation == DecisionExplanation(
        summary=(
            "Software developer is a strong match."
        ),
        reasons=[
            "You have all the essential skills "
            "required for this occupation.",
        ],
    )
    
def test_no_match_can_be_explained(
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

    explainer = DecisionExplainer()

    explanation = explainer.explain(
        match,
    )

    assert explanation == DecisionExplanation(
        summary=(
            "Software developer is not a match."
        ),
        reasons=[
            "You are missing the essential skill: Python.",
        ],
    )
    
def test_recommendations_can_be_explained(
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

    engine = SkillRecommendationEngine(
        analyzer,
    )

    result = engine.recommend_skills(
        occupation_id="software-developer",
        candidate_skills=["python"],
    )

    explainer = RecommendationExplainer()

    explanation = explainer.explain_result(
        result,
    )

    assert explanation == RecommendationExplanation(
        summary=(
            "1 skill is recommended: "
            "Docker (essential)."
        ),
        reasons=[
            "This skill is essential for the target occupation.",
            "This skill is missing from your current skills.",
        ],
    )
    
def test_learning_path_can_be_explained(
    tmp_path,
):

    database = tmp_path / "career_agent.db"

    knowledge = Knowledge(
        skills=[
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
            OccupationSkillRelation(
                occupation_id="software-developer",
                skill_id="kubernetes",
                relation_type="essential",
            ),
        ],
        skill_dependencies=[
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
        occupation_id="software-developer",
        candidate_skills=[],
    )

    explainer = LearningPathExplainer()

    dependencies = [
        SkillDependency(
            prerequisite_skill_id="docker",
            dependent_skill_id="kubernetes",
        ),
    ]

    explanation = explainer.explain(
        learning_path,
        dependencies,
    )

    assert explanation == LearningPathExplanation(
        summary=(
            "Learning path with 2 skills: "
            "Docker (essential) and Kubernetes (essential)."
        ),
        reasons=[
            "Docker should be learned before Kubernetes because it is a prerequisite.",
        ],
    )
    
def test_learning_path_preserves_prerequisite_dependencies(
    tmp_path,
):

    database = tmp_path / "career_agent.db"

    knowledge = Knowledge(
        skills=[
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
            OccupationSkillRelation(
                occupation_id="software-developer",
                skill_id="kubernetes",
                relation_type="essential",
            ),
        ],
        skill_dependencies=[
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
        occupation_id="software-developer",
        candidate_skills=[],
    )

    assert learning_path.dependencies == [
        SkillDependency(
            prerequisite_skill_id="docker",
            dependent_skill_id="kubernetes",
        ),
    ]

    assert learning_path == LearningPath(
        steps=[
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
        dependencies=[
            SkillDependency(
                prerequisite_skill_id="docker",
                dependent_skill_id="kubernetes",
            ),
        ],
    )
    
def test_learning_path_explainer_uses_dependencies_from_learning_path():

    learning_path = LearningPath(
        steps=[
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
        dependencies=[
            SkillDependency(
                prerequisite_skill_id="docker",
                dependent_skill_id="kubernetes",
            ),
        ],
    )

    explainer = LearningPathExplainer()

    explanation = explainer.explain(
        learning_path,
    )

    assert explanation == LearningPathExplanation(
        summary=(
            "Learning path with 2 skills: "
            "Docker (essential) and Kubernetes (essential)."
        ),
        reasons=[
            "Docker should be learned before Kubernetes because it is a prerequisite.",
        ],
    )
    
def test_learning_path_without_dependencies_has_no_dependency_reasons():

    learning_path = LearningPath(
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

    explainer = LearningPathExplainer()

    explanation = explainer.explain(
        learning_path,
    )

    assert explanation == LearningPathExplanation(
        summary=(
            "Learning path with 1 skill: "
            "Python (essential)."
        ),
        reasons=[],
    )
    
def test_plan_preserves_transitive_dependencies(
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
        
    assert learning_path.dependencies == [
        SkillDependency(
            prerequisite_skill_id="git",
            dependent_skill_id="docker",
        ),
        SkillDependency(
            prerequisite_skill_id="docker",
            dependent_skill_id="kubernetes",
        ),
    ]
    
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
    
    assert learning_path.dependencies == [
        SkillDependency(
            prerequisite_skill_id="git",
            dependent_skill_id="docker",
        ),
        SkillDependency(
            prerequisite_skill_id="git",
            dependent_skill_id="linux",
        ),
    ]