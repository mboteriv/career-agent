

from career_agent.models.decision_explanation import DecisionExplanation
from career_agent.models.occupation_match import OccupationMatch
from career_agent.models.recommendation_explanation import RecommendationExplanation
from career_agent.models.recommendation_priority import RecommendationPriority
from career_agent.models.semantic_entity import SemanticEntity
from career_agent.models.skill_gap import SkillGap
from career_agent.models.skill_recommendation import SkillRecommendation
from career_agent.services.decision_explainer import DecisionExplainer
from career_agent.services.recommendation_explainer import RecommendationExplainer


def test_explain_returns_full_match_explanation():

    match = OccupationMatch(
        occupation=SemanticEntity(
            id="software-developer",
            preferred_label="Software developer",
        ),
        score=1.0,
        skill_gap=SkillGap(
            total_essential=2,
            total_optional=1,
        ),
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
            "You have all the essential skills required for this occupation."
        ],
    )
    
def test_explain_identifies_missing_essential_skill():

    match = OccupationMatch(
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
        ),
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
            "You are missing the essential skill: Python."
        ],
    )
def test_explain_identifies_multiple_missing_essential_skills():

    match = OccupationMatch(
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
                SemanticEntity(
                    id="docker",
                    preferred_label="Docker",
                ),
            ],
            total_essential=2,
        ),
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
            "You are missing the essential skills: Python and Docker.",
        ],
    )
    
def test_explain_identifies_partial_match():

    match = OccupationMatch(
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
        ),
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
    
def test_explain_identifies_missing_optional_skill():

    match = OccupationMatch(
        occupation=SemanticEntity(
            id="software-developer",
            preferred_label="Software developer",
        ),
        score=1.0,
        skill_gap=SkillGap(
            missing_optional=[
                SemanticEntity(
                    id="kubernetes",
                    preferred_label="Kubernetes",
                ),
            ],
            total_essential=2,
            total_optional=1,
        ),
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
            "You are missing the optional skill: Kubernetes.",
        ],
    )
    
def test_explain_formats_multiple_missing_skills_with_commas():

    match = OccupationMatch(
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
                SemanticEntity(
                    id="docker",
                    preferred_label="Docker",
                ),
                SemanticEntity(
                    id="kubernetes",
                    preferred_label="Kubernetes",
                ),
            ],
            total_essential=3,
        ),
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
            "You are missing the essential skills: "
            "Python, Docker and Kubernetes.",
        ],
    )
    
def test_explain_partial_match_with_multiple_missing_skills():

    match = OccupationMatch(
        occupation=SemanticEntity(
            id="software-developer",
            preferred_label="Software developer",
        ),
        score=0.66,
        skill_gap=SkillGap(
            missing_essential=[
                SemanticEntity(
                    id="docker",
                    preferred_label="Docker",
                ),
            ],
            total_essential=3,
        ),
    )

    explainer = DecisionExplainer()

    explanation = explainer.explain(
        match,
    )

    assert explanation == DecisionExplanation(
        summary=(
            "Software developer is a partial match (66%)."
        ),
        reasons=[
            "You are missing the essential skill: Docker.",
        ],
    )
    
def test_explain_includes_percentage_in_partial_match_summary():

    match = OccupationMatch(
        occupation=SemanticEntity(
            id="software-developer",
            preferred_label="Software developer",
        ),
        score=0.66,
        skill_gap=SkillGap(
            missing_essential=[
                SemanticEntity(
                    id="docker",
                    preferred_label="Docker",
                ),
            ],
            total_essential=3,
        ),
    )

    explainer = DecisionExplainer()

    explanation = explainer.explain(
        match,
    )

    assert explanation == DecisionExplanation(
        summary=(
            "Software developer is a partial match (66%)."
        ),
        reasons=[
            "You are missing the essential skill: Docker.",
        ],
    )
    
def test_explain_handles_occupation_without_essential_skills():

    match = OccupationMatch(
        occupation=SemanticEntity(
            id="software-developer",
            preferred_label="Software developer",
        ),
        score=1.0,
        skill_gap=SkillGap(),
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
    
def test_explain_identifies_multiple_missing_optional_skills():

    match = OccupationMatch(
        occupation=SemanticEntity(
            id="software-developer",
            preferred_label="Software developer",
        ),
        score=1.0,
        skill_gap=SkillGap(
            missing_optional=[
                SemanticEntity(
                    id="kubernetes",
                    preferred_label="Kubernetes",
                ),
                SemanticEntity(
                    id="terraform",
                    preferred_label="Terraform",
                ),
                SemanticEntity(
                    id="aws",
                    preferred_label="AWS",
                ),
            ],
            total_essential=3,
            total_optional=3,
        ),
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
            "You are missing the optional skills: "
            "Kubernetes, Terraform and AWS.",
        ],
    )
    
def test_explain_treats_score_below_one_as_partial_match():

    match = OccupationMatch(
        occupation=SemanticEntity(
            id="software-developer",
            preferred_label="Software developer",
        ),
        score=0.99,
        skill_gap=SkillGap(
            missing_essential=[
                SemanticEntity(
                    id="docker",
                    preferred_label="Docker",
                ),
            ],
            total_essential=100,
        ),
    )

    explainer = DecisionExplainer()

    explanation = explainer.explain(
        match,
    )

    assert explanation == DecisionExplanation(
        summary=(
            "Software developer is a partial match (99%)."
        ),
        reasons=[
            "You are missing the essential skill: Docker.",
        ],
    )
    
def test_explain_treats_small_positive_score_as_partial_match():

    match = OccupationMatch(
        occupation=SemanticEntity(
            id="software-developer",
            preferred_label="Software developer",
        ),
        score=0.01,
        skill_gap=SkillGap(
            missing_essential=[
                SemanticEntity(
                    id="docker",
                    preferred_label="Docker",
                ),
            ],
            total_essential=100,
        ),
    )

    explainer = DecisionExplainer()

    explanation = explainer.explain(
        match,
    )

    assert explanation == DecisionExplanation(
        summary=(
            "Software developer is a partial match (1%)."
        ),
        reasons=[
            "You are missing the essential skill: Docker.",
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