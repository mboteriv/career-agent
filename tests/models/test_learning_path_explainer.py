


from career_agent.models.learning_path import LearningPath
from career_agent.models.learning_path_explanation import LearningPathExplanation
from career_agent.models.recommendation_priority import RecommendationPriority
from career_agent.models.semantic_entity import SemanticEntity
from career_agent.models.skill_dependency import SkillDependency
from career_agent.models.skill_recommendation import SkillRecommendation
from career_agent.services.learning_path_explainer import LearningPathExplainer


def test_explain_returns_single_step_learning_path():

    learning_path = LearningPath(
        steps=[
            SkillRecommendation(
                skill=SemanticEntity(
                    id="docker",
                    preferred_label="Docker",
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
        summary="Learning path with 1 skill: Docker (essential).",
        reasons=[],
    )
    
def test_explain_returns_multiple_step_learning_path():

    learning_path = LearningPath(
        steps=[
            SkillRecommendation(
                skill=SemanticEntity(
                    id="python",
                    preferred_label="Python",
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
                priority=RecommendationPriority.OPTIONAL,
            ),
        ],
    )

    explainer = LearningPathExplainer()

    explanation = explainer.explain(
        learning_path,
    )

    assert explanation == LearningPathExplanation(
        summary=(
            "Learning path with 3 skills: "
            "Python (essential), Docker (essential) "
            "and Kubernetes (optional)."
        ),
        reasons=[],
    )
    
def test_explain_returns_empty_learning_path():

    learning_path = LearningPath(
        steps=[],
    )

    explainer = LearningPathExplainer()

    explanation = explainer.explain(
        learning_path,
    )

    assert explanation == LearningPathExplanation(
        summary="No skills are included in the learning path.",
        reasons=[],
    )
    
def test_explain_identifies_prerequisite_relationship():

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
    )

    dependencies = [
        SkillDependency(
            prerequisite_skill_id="docker",
            dependent_skill_id="kubernetes",
        ),
    ]

    explainer = LearningPathExplainer()

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
    
def test_explain_identifies_transitive_prerequisite_relationships():

    learning_path = LearningPath(
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

    dependencies = [
        SkillDependency(
            prerequisite_skill_id="git",
            dependent_skill_id="docker",
        ),
        SkillDependency(
            prerequisite_skill_id="docker",
            dependent_skill_id="kubernetes",
        ),
    ]

    explainer = LearningPathExplainer()

    explanation = explainer.explain(
        learning_path,
        dependencies,
    )

    assert explanation == LearningPathExplanation(
        summary=(
            "Learning path with 3 skills: "
            "Git (essential), Docker (essential) "
            "and Kubernetes (essential)."
        ),
        reasons=[
            "Git should be learned before Docker because it is a prerequisite.",
            "Docker should be learned before Kubernetes because it is a prerequisite.",
        ],
    )
    
def test_explain_handles_prerequisite_not_in_learning_path():

    learning_path = LearningPath(
        steps=[
            SkillRecommendation(
                skill=SemanticEntity(
                    id="docker",
                    preferred_label="Docker",
                ),
            priority=RecommendationPriority.ESSENTIAL,
            ),
        ],
    )

    dependencies = [
        SkillDependency(
            prerequisite_skill_id="git",
            dependent_skill_id="docker",
        ),
    ]

    explainer = LearningPathExplainer()

    explanation = explainer.explain(
        learning_path,
        dependencies,
    )

    assert explanation == LearningPathExplanation(
        summary=(
            "Learning path with 1 skill: "
            "Docker (essential)."
        ),
        reasons=[
            "git should be learned before Docker because it is a prerequisite.",
        ],
    )
    
def test_explain_ignores_irrelevant_dependencies():

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
    )

    dependencies = [
        SkillDependency(
            prerequisite_skill_id="docker",
            dependent_skill_id="kubernetes",
        ),
        SkillDependency(
            prerequisite_skill_id="git",
            dependent_skill_id="python",
        ),
    ]

    explainer = LearningPathExplainer()

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
    
def test_explain_does_not_duplicate_dependency_reasons():

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
    )

    dependencies = [
        SkillDependency(
            prerequisite_skill_id="docker",
            dependent_skill_id="kubernetes",
        ),
        SkillDependency(
            prerequisite_skill_id="docker",
            dependent_skill_id="kubernetes",
        ),
    ]

    explainer = LearningPathExplainer()

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
    
def test_explain_orders_dependency_reasons_by_learning_path():

    learning_path = LearningPath(
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

    dependencies = [
        SkillDependency(
            prerequisite_skill_id="docker",
            dependent_skill_id="kubernetes",
        ),
        SkillDependency(
            prerequisite_skill_id="git",
            dependent_skill_id="docker",
        ),
    ]

    explainer = LearningPathExplainer()

    explanation = explainer.explain(
        learning_path,
        dependencies,
    )

    assert explanation == LearningPathExplanation(
        summary=(
            "Learning path with 3 skills: "
            "Git (essential), Docker (essential) "
            "and Kubernetes (essential)."
        ),
        reasons=[
            "Git should be learned before Docker because it is a prerequisite.",
            "Docker should be learned before Kubernetes because it is a prerequisite.",
        ],
    )
    
def test_explain_ignores_dependency_with_dependent_skill_outside_path():

    learning_path = LearningPath(
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

    dependencies = [
        SkillDependency(
            prerequisite_skill_id="git",
            dependent_skill_id="kubernetes",
        ),
    ]

    explainer = LearningPathExplainer()

    explanation = explainer.explain(
        learning_path,
        dependencies,
    )

    assert explanation == LearningPathExplanation(
        summary=(
            "Learning path with 2 skills: "
            "Git (essential) and Docker (essential)."
        ),
        reasons=[],
    )
    
def test_explain_identifies_multiple_prerequisites_for_same_skill():

    learning_path = LearningPath(
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
                    id="linux",
                    preferred_label="Linux",
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

    dependencies = [
        SkillDependency(
            prerequisite_skill_id="git",
            dependent_skill_id="docker",
        ),
        SkillDependency(
            prerequisite_skill_id="linux",
            dependent_skill_id="docker",
        ),
    ]

    explainer = LearningPathExplainer()

    explanation = explainer.explain(
        learning_path,
        dependencies,
    )

    assert explanation == LearningPathExplanation(
        summary=(
            "Learning path with 3 skills: "
            "Git (essential), Linux (essential) "
            "and Docker (essential)."
        ),
        reasons=[
            "Git should be learned before Docker because it is a prerequisite.",
            "Linux should be learned before Docker because it is a prerequisite.",
        ],
    )