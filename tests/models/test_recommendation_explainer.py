from career_agent.models.recommendation_explanation import RecommendationExplanation
from career_agent.models.recommendation_priority import RecommendationPriority
from career_agent.models.semantic_entity import SemanticEntity
from career_agent.models.skill_recommendation import SkillRecommendation
from career_agent.services.recommendation_explainer import RecommendationExplainer
from career_agent.models.skill_recommendation_result import SkillRecommendationResult


def test_explain_returns_essential_skill_recommendation():

    recommendation = SkillRecommendation(
        skill=SemanticEntity(
            id="docker",
            preferred_label="Docker",
        ),
        priority=RecommendationPriority.ESSENTIAL,
    )

    explainer = RecommendationExplainer()

    explanation = explainer.explain(
        recommendation,
    )

    assert explanation == RecommendationExplanation(
        summary="Docker is an essential skill to learn.",
        reasons=[
            "This skill is essential for the target occupation.",
            "This skill is missing from your current skills.",
        ],
    )
    
def test_explain_returns_optional_skill_recommendation():

    recommendation = SkillRecommendation(
        skill=SemanticEntity(
            id="kubernetes",
            preferred_label="Kubernetes",
        ),
        priority=RecommendationPriority.OPTIONAL,
    )

    explainer = RecommendationExplainer()

    explanation = explainer.explain(
        recommendation,
    )

    assert explanation == RecommendationExplanation(
        summary="Kubernetes is an optional skill to learn.",
        reasons=[
            "This skill is optional for the target occupation.",
            "This skill is missing from your current skills.",
        ],
    )
    
def test_explain_preserves_skill_label():

    recommendation = SkillRecommendation(
        skill=SemanticEntity(
            id="machine-learning",
            preferred_label="Machine Learning",
        ),
        priority=RecommendationPriority.ESSENTIAL,
    )

    explainer = RecommendationExplainer()

    explanation = explainer.explain(
        recommendation,
    )

    assert explanation == RecommendationExplanation(
        summary="Machine Learning is an essential skill to learn.",
        reasons=[
            "This skill is essential for the target occupation.",
            "This skill is missing from your current skills.",
        ],
    )
    
def test_explain_result_summarizes_recommendations():

    result = SkillRecommendationResult(
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

    explainer = RecommendationExplainer()

    explanation = explainer.explain_result(
        result,
    )

    assert explanation == RecommendationExplanation(
        summary=(
            "3 skills are recommended: "
            "Python (essential), Docker (essential) "
            "and Kubernetes (optional)."
        ),
        reasons=[
            "This skill is essential for the target occupation.",
            "This skill is missing from your current skills.",
            "This skill is essential for the target occupation.",
            "This skill is missing from your current skills.",
            "This skill is optional for the target occupation.",
            "This skill is missing from your current skills.",
        ],
    )
    
def test_explain_empty_result():

    result = SkillRecommendationResult(
        recommendations=[],
    )

    explainer = RecommendationExplainer()

    explanation = explainer.explain_result(
        result,
    )

    assert explanation == RecommendationExplanation(
        summary="No skills are recommended.",
        reasons=[],
    )

def test_explain_single_recommendation():

    result = SkillRecommendationResult(
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

    explainer = RecommendationExplainer()

    explanation = explainer.explain_result(
        result,
    )

    assert explanation == RecommendationExplanation(
        summary=(
            "1 skill is recommended: Python (essential)."
        ),
        reasons=[
            "This skill is essential for the target occupation.",
            "This skill is missing from your current skills.",
        ],
    )
    
def test_explain_single_optional_recommendation():

    result = SkillRecommendationResult(
        recommendations=[
            SkillRecommendation(
                skill=SemanticEntity(
                    id="kubernetes",
                    preferred_label="Kubernetes",
                ),
                priority=RecommendationPriority.OPTIONAL,
            ),
        ],
    )

    explainer = RecommendationExplainer()

    explanation = explainer.explain_result(
        result,
    )

    assert explanation == RecommendationExplanation(
        summary=(
            "1 skill is recommended: Kubernetes (optional)."
        ),
        reasons=[
            "This skill is optional for the target occupation.",
            "This skill is missing from your current skills.",
        ],
    )

def test_explain_result_includes_single_recommended_skill():

    result = SkillRecommendationResult(
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

    explainer = RecommendationExplainer()

    explanation = explainer.explain_result(
        result,
    )

    assert explanation == RecommendationExplanation(
        summary=(
            "1 skill is recommended: Python (essential)."
        ),
        reasons=[
            "This skill is essential for the target occupation.",
            "This skill is missing from your current skills.",
        ],
    )
    
def test_explain_result_includes_multiple_recommended_skills():

    result = SkillRecommendationResult(
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

    explainer = RecommendationExplainer()

    explanation = explainer.explain_result(
        result,
    )

    assert explanation == RecommendationExplanation(
        summary=(
            "3 skills are recommended: "
            "Python (essential), Docker (essential) "
            "and Kubernetes (optional)."
        ),
        reasons=[
            "This skill is essential for the target occupation.",
            "This skill is missing from your current skills.",
            "This skill is essential for the target occupation.",
            "This skill is missing from your current skills.",
            "This skill is optional for the target occupation.",
            "This skill is missing from your current skills.",
        ],
    )
    
def test_explain_result_formats_multiple_recommendations_with_commas():

    result = SkillRecommendationResult(
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
            SkillRecommendation(
                skill=SemanticEntity(
                    id="terraform",
                    preferred_label="Terraform",
                ),
                priority=RecommendationPriority.OPTIONAL,
            ),
        ],
    )

    explainer = RecommendationExplainer()

    explanation = explainer.explain_result(
        result,
    )

    assert explanation == RecommendationExplanation(
        summary=(
            "4 skills are recommended: "
            "Python (essential), Docker (essential), "
            "Kubernetes (optional) and Terraform (optional)."
        ),
        reasons=[
            "This skill is essential for the target occupation.",
            "This skill is missing from your current skills.",
            "This skill is essential for the target occupation.",
            "This skill is missing from your current skills.",
            "This skill is optional for the target occupation.",
            "This skill is missing from your current skills.",
            "This skill is optional for the target occupation.",
            "This skill is missing from your current skills.",
        ],
    )
    
def test_explain_identifies_skill_as_missing():

    recommendation = SkillRecommendation(
        skill=SemanticEntity(
            id="docker",
            preferred_label="Docker",
        ),
        priority=RecommendationPriority.ESSENTIAL,
    )

    explainer = RecommendationExplainer()

    explanation = explainer.explain(
        recommendation,
    )

    assert explanation == RecommendationExplanation(
        summary="Docker is an essential skill to learn.",
        reasons=[
            "This skill is essential for the target occupation.",
            "This skill is missing from your current skills.",
        ],
    )
    
def test_explain_result_includes_recommendation_reason():

    result = SkillRecommendationResult(
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

    explainer = RecommendationExplainer()

    explanation = explainer.explain_result(
        result,
    )

    assert explanation == RecommendationExplanation(
        summary=(
            "1 skill is recommended: Python (essential)."
        ),
        reasons=[
            "This skill is essential for the target occupation.",
            "This skill is missing from your current skills.",
        ],
    )
    
def test_explain_result_includes_reasons_for_multiple_recommendations():

    result = SkillRecommendationResult(
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
                    id="kubernetes",
                    preferred_label="Kubernetes",
                ),
                priority=RecommendationPriority.OPTIONAL,
            ),
        ],
    )

    explainer = RecommendationExplainer()

    explanation = explainer.explain_result(
        result,
    )

    assert explanation == RecommendationExplanation(
        summary=(
            "2 skills are recommended: "
            "Python (essential) and Kubernetes (optional)."
        ),
        reasons=[
            "This skill is essential for the target occupation.",
            "This skill is missing from your current skills.",
            "This skill is optional for the target occupation.",
            "This skill is missing from your current skills.",
        ],
    )