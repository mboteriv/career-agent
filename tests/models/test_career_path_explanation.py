from career_agent.models.career_path import CareerPath
from career_agent.models.career_path_explanation import CareerPathExplanation
from career_agent.models.occupation_match import OccupationMatch
from career_agent.models.semantic_entity import SemanticEntity
from career_agent.models.skill_gap import SkillGap
from career_agent.services.career_path_explainer import CareerPathExplainer


def test_explain_prefers_occupation_with_fewer_missing_essential_skills():

    career_path = CareerPath(
        occupations=[
            OccupationMatch(
                occupation=SemanticEntity(
                    id="data-analyst",
                    preferred_label="Data Analyst",
                ),
                score=0.8,
                skill_gap=SkillGap(
                    missing_essential=[
                        SemanticEntity(
                            id="sql",
                            preferred_label="SQL",
                        ),
                    ],
                    total_essential=5,
                ),
            ),
            OccupationMatch(
                occupation=SemanticEntity(
                    id="data-engineer",
                    preferred_label="Data Engineer",
                ),
                score=0.6,
                skill_gap=SkillGap(
                    missing_essential=[
                        SemanticEntity(
                            id="spark",
                            preferred_label="Spark",
                        ),
                        SemanticEntity(
                            id="kafka",
                            preferred_label="Kafka",
                        ),
                    ],
                    total_essential=5,
                ),
            ),
        ],
    )

    explainer = CareerPathExplainer()

    explanation = explainer.explain(
        career_path,
    )

    assert explanation == CareerPathExplanation(
        summary=(
            "Data Analyst appears before Data Engineer "
            "because it requires fewer additional skills."
        ),
        reasons=[
            "Data Analyst requires 1 additional essential skill.",
            "Data Engineer requires 2 additional essential skills.",
        ],
    )
    
def test_explain_occupation_with_no_missing_essential_skills():

    career_path = CareerPath(
        occupations=[
            OccupationMatch(
                occupation=SemanticEntity(
                    id="software-developer",
                    preferred_label="Software Developer",
                ),
                score=1.0,
                skill_gap=SkillGap(
                    missing_essential=[],
                    total_essential=5,
                ),
            ),
        ],
    )

    explainer = CareerPathExplainer()

    explanation = explainer.explain(
        career_path,
    )

    assert explanation == CareerPathExplanation(
        summary=(
            "Software Developer is the strongest match."
        ),
        reasons=[
            "Software Developer requires 0 additional essential skills.",
        ],
    )
    
def test_explain_single_occupation_with_multiple_missing_essential_skills():

    career_path = CareerPath(
        occupations=[
            OccupationMatch(
                occupation=SemanticEntity(
                    id="software-developer",
                    preferred_label="Software Developer",
                ),
                score=0.6,
                skill_gap=SkillGap(
                    missing_essential=[
                        SemanticEntity(
                            id="docker",
                            preferred_label="Docker",
                        ),
                        SemanticEntity(
                            id="kubernetes",
                            preferred_label="Kubernetes",
                        ),
                    ],
                    total_essential=5,
                ),
            ),
        ],
    )

    explainer = CareerPathExplainer()

    explanation = explainer.explain(
        career_path,
    )

    assert explanation == CareerPathExplanation(
        summary="Software Developer is the strongest match.",
        reasons=[
            "Software Developer requires 2 additional essential skills.",
        ],
    )
    
def test_explain_empty_career_path():

    career_path = CareerPath(
        occupations=[],
    )

    explainer = CareerPathExplainer()

    explanation = explainer.explain(
        career_path,
    )

    assert explanation == CareerPathExplanation(
        summary="No occupations were found.",
        reasons=[],
    )
    
def test_explain_preserves_career_path_order():

    career_path = CareerPath(
        occupations=[
            OccupationMatch(
                occupation=SemanticEntity(
                    id="data-engineer",
                    preferred_label="Data Engineer",
                ),
                score=0.6,
                skill_gap=SkillGap(
                    missing_essential=[
                        SemanticEntity(
                            id="spark",
                            preferred_label="Spark",
                        ),
                        SemanticEntity(
                            id="kafka",
                            preferred_label="Kafka",
                        ),
                    ],
                    total_essential=5,
                ),
            ),
            OccupationMatch(
                occupation=SemanticEntity(
                    id="data-analyst",
                    preferred_label="Data Analyst",
                ),
                score=0.8,
                skill_gap=SkillGap(
                    missing_essential=[
                        SemanticEntity(
                            id="sql",
                            preferred_label="SQL",
                        ),
                    ],
                    total_essential=5,
                ),
            ),
        ],
    )

    explainer = CareerPathExplainer()

    explanation = explainer.explain(
        career_path,
    )

    assert explanation == CareerPathExplanation(
        summary=(
            "Data Engineer appears before Data Analyst."
        ),
        reasons=[
            "Data Engineer requires 2 additional essential skills.",
            "Data Analyst requires 1 additional essential skill.",
        ],
    )
    
def test_explain_does_not_claim_fewer_skills_when_first_occupation_has_more():

    career_path = CareerPath(
        occupations=[
            OccupationMatch(
                occupation=SemanticEntity(
                    id="data-engineer",
                    preferred_label="Data Engineer",
                ),
                score=0.6,
                skill_gap=SkillGap(
                    missing_essential=[
                        SemanticEntity(
                            id="spark",
                            preferred_label="Spark",
                        ),
                        SemanticEntity(
                            id="kafka",
                            preferred_label="Kafka",
                        ),
                    ],
                    total_essential=5,
                ),
            ),
            OccupationMatch(
                occupation=SemanticEntity(
                    id="data-analyst",
                    preferred_label="Data Analyst",
                ),
                score=0.8,
                skill_gap=SkillGap(
                    missing_essential=[
                        SemanticEntity(
                            id="sql",
                            preferred_label="SQL",
                        ),
                    ],
                    total_essential=5,
                ),
            ),
        ],
    )

    explainer = CareerPathExplainer()

    explanation = explainer.explain(
        career_path,
    )

    assert explanation == CareerPathExplanation(
        summary=(
            "Data Engineer appears before Data Analyst."
        ),
        reasons=[
            "Data Engineer requires 2 additional essential skills.",
            "Data Analyst requires 1 additional essential skill.",
        ],
    )
    
def test_explain_equal_missing_skills_does_not_claim_fewer():

    career_path = CareerPath(
        occupations=[
            OccupationMatch(
                occupation=SemanticEntity(
                    id="data-analyst",
                    preferred_label="Data Analyst",
                ),
                score=0.8,
                skill_gap=SkillGap(
                    missing_essential=[
                        SemanticEntity(
                            id="sql",
                            preferred_label="SQL",
                        ),
                        SemanticEntity(
                            id="python",
                            preferred_label="Python",
                        ),
                    ],
                    total_essential=5,
                ),
            ),
            OccupationMatch(
                occupation=SemanticEntity(
                    id="data-engineer",
                    preferred_label="Data Engineer",
                ),
                score=0.8,
                skill_gap=SkillGap(
                    missing_essential=[
                        SemanticEntity(
                            id="spark",
                            preferred_label="Spark",
                        ),
                        SemanticEntity(
                            id="kafka",
                            preferred_label="Kafka",
                        ),
                    ],
                    total_essential=5,
                ),
            ),
        ],
    )

    explainer = CareerPathExplainer()

    explanation = explainer.explain(
        career_path,
    )

    assert explanation == CareerPathExplanation(
        summary=(
            "Data Analyst appears before Data Engineer."
        ),
        reasons=[
            "Data Analyst requires 2 additional essential skills.",
            "Data Engineer requires 2 additional essential skills.",
        ],
    )
    
def test_explain_prefers_occupation_with_fewer_missing_optional_skills():

    career_path = CareerPath(
        occupations=[
            OccupationMatch(
                occupation=SemanticEntity(
                    id="data-analyst",
                    preferred_label="Data Analyst",
                ),
                score=0.8,
                skill_gap=SkillGap(
                    missing_essential=[
                        SemanticEntity(
                            id="sql",
                            preferred_label="SQL",
                        ),
                    ],
                    missing_optional=[
                        SemanticEntity(
                            id="tableau",
                            preferred_label="Tableau",
                        ),
                    ],
                    total_essential=5,
                    total_optional=3,
                ),
            ),
            OccupationMatch(
                occupation=SemanticEntity(
                    id="data-engineer",
                    preferred_label="Data Engineer",
                ),
                score=0.8,
                skill_gap=SkillGap(
                    missing_essential=[
                        SemanticEntity(
                            id="python",
                            preferred_label="Python",
                        ),
                    ],
                    missing_optional=[
                        SemanticEntity(
                            id="spark",
                            preferred_label="Spark",
                        ),
                        SemanticEntity(
                            id="kafka",
                            preferred_label="Kafka",
                        ),
                    ],
                    total_essential=5,
                    total_optional=3,
                ),
            ),
        ],
    )

    explainer = CareerPathExplainer()

    explanation = explainer.explain(
        career_path,
    )

    assert explanation == CareerPathExplanation(
        summary=(
            "Data Analyst appears before Data Engineer "
            "because it requires fewer additional skills."
        ),
        reasons=[
            "Data Analyst requires 1 additional essential skill.",
            "Data Engineer requires 1 additional essential skill.",
        ],
    )
    
def test_explain_does_not_claim_fewer_skills_when_total_is_equal():

    career_path = CareerPath(
        occupations=[
            OccupationMatch(
                occupation=SemanticEntity(
                    id="data-analyst",
                    preferred_label="Data Analyst",
                ),
                score=0.8,
                skill_gap=SkillGap(
                    missing_essential=[
                        SemanticEntity(
                            id="sql",
                            preferred_label="SQL",
                        ),
                    ],
                    missing_optional=[
                        SemanticEntity(
                            id="tableau",
                            preferred_label="Tableau",
                        ),
                    ],
                    total_essential=5,
                    total_optional=3,
                ),
            ),
            OccupationMatch(
                occupation=SemanticEntity(
                    id="data-engineer",
                    preferred_label="Data Engineer",
                ),
                score=0.6,
                skill_gap=SkillGap(
                    missing_essential=[
                        SemanticEntity(
                            id="python",
                            preferred_label="Python",
                        ),
                    ],
                    missing_optional=[
                        SemanticEntity(
                            id="spark",
                            preferred_label="Spark",
                        ),
                    ],
                    total_essential=5,
                    total_optional=3,
                ),
            ),
        ],
    )

    explainer = CareerPathExplainer()

    explanation = explainer.explain(
        career_path,
    )

    assert explanation == CareerPathExplanation(
        summary=(
            "Data Analyst appears before Data Engineer "
            "because it is a stronger match."
        ),
        reasons=[
            "Data Analyst requires 1 additional essential skill.",
            "Data Engineer requires 1 additional essential skill.",
            "Data Analyst has a match score of 80%.",
            "Data Engineer has a match score of 60%.",
        ],
    )
    
def test_explain_prefers_higher_match_score_when_missing_skills_are_equal():

    career_path = CareerPath(
        occupations=[
            OccupationMatch(
                occupation=SemanticEntity(
                    id="data-analyst",
                    preferred_label="Data Analyst",
                ),
                score=0.8,
                skill_gap=SkillGap(
                    missing_essential=[
                        SemanticEntity(
                            id="sql",
                            preferred_label="SQL",
                        ),
                    ],
                    total_essential=5,
                ),
            ),
            OccupationMatch(
                occupation=SemanticEntity(
                    id="data-engineer",
                    preferred_label="Data Engineer",
                ),
                score=0.6,
                skill_gap=SkillGap(
                    missing_essential=[
                        SemanticEntity(
                            id="python",
                            preferred_label="Python",
                        ),
                    ],
                    total_essential=5,
                ),
            ),
        ],
    )

    explainer = CareerPathExplainer()

    explanation = explainer.explain(
        career_path,
    )

    assert explanation == CareerPathExplanation(
        summary=(
            "Data Analyst appears before Data Engineer "
            "because it is a stronger match."
        ),
        reasons=[
            "Data Analyst requires 1 additional essential skill.",
            "Data Engineer requires 1 additional essential skill.",
            "Data Analyst has a match score of 80%.",
            "Data Engineer has a match score of 60%.",
        ],
    )
    
def test_explain_equal_missing_skills_and_score():

    career_path = CareerPath(
        occupations=[
            OccupationMatch(
                occupation=SemanticEntity(
                    id="data-analyst",
                    preferred_label="Data Analyst",
                ),
                score=0.8,
                skill_gap=SkillGap(
                    missing_essential=[
                        SemanticEntity(
                            id="sql",
                            preferred_label="SQL",
                        ),
                    ],
                    total_essential=5,
                ),
            ),
            OccupationMatch(
                occupation=SemanticEntity(
                    id="data-engineer",
                    preferred_label="Data Engineer",
                ),
                score=0.8,
                skill_gap=SkillGap(
                    missing_essential=[
                        SemanticEntity(
                            id="python",
                            preferred_label="Python",
                        ),
                    ],
                    total_essential=5,
                ),
            ),
        ],
    )

    explainer = CareerPathExplainer()

    explanation = explainer.explain(
        career_path,
    )

    assert explanation == CareerPathExplanation(
        summary=(
            "Data Analyst appears before Data Engineer."
        ),
        reasons=[
            "Data Analyst requires 1 additional essential skill.",
            "Data Engineer requires 1 additional essential skill.",
        ],
    )
    
def test_explain_only_compares_first_two_occupations():

    career_path = CareerPath(
        occupations=[
            OccupationMatch(
                occupation=SemanticEntity(
                    id="data-analyst",
                    preferred_label="Data Analyst",
                ),
                score=0.8,
                skill_gap=SkillGap(
                    missing_essential=[
                        SemanticEntity(
                            id="sql",
                            preferred_label="SQL",
                        ),
                    ],
                    total_essential=5,
                ),
            ),
            OccupationMatch(
                occupation=SemanticEntity(
                    id="data-engineer",
                    preferred_label="Data Engineer",
                ),
                score=0.6,
                skill_gap=SkillGap(
                    missing_essential=[
                        SemanticEntity(
                            id="python",
                            preferred_label="Python",
                        ),
                        SemanticEntity(
                            id="spark",
                            preferred_label="Spark",
                        ),
                    ],
                    total_essential=5,
                ),
            ),
            OccupationMatch(
                occupation=SemanticEntity(
                    id="devops-engineer",
                    preferred_label="DevOps Engineer",
                ),
                score=0.4,
                skill_gap=SkillGap(
                    missing_essential=[
                        SemanticEntity(
                            id="kubernetes",
                            preferred_label="Kubernetes",
                        ),
                    ],
                    total_essential=5,
                ),
            ),
        ],
    )

    explainer = CareerPathExplainer()

    explanation = explainer.explain(
        career_path,
    )

    assert explanation == CareerPathExplanation(
        summary=(
            "Data Analyst appears before Data Engineer "
            "because it requires fewer additional skills."
        ),
        reasons=[
            "Data Analyst requires 1 additional essential skill.",
            "Data Engineer requires 2 additional essential skills.",
        ],
    )
    
def test_explain_prefers_match_score_over_missing_skills_when_ordered_by_score():

    career_path = CareerPath(
        occupations=[
            OccupationMatch(
                occupation=SemanticEntity(
                    id="data-analyst",
                    preferred_label="Data Analyst",
                ),
                score=0.8,
                skill_gap=SkillGap(
                    missing_essential=[
                        SemanticEntity(
                            id="sql",
                            preferred_label="SQL",
                        ),
                        SemanticEntity(
                            id="python",
                            preferred_label="Python",
                        ),
                    ],
                    total_essential=5,
                ),
            ),
            OccupationMatch(
                occupation=SemanticEntity(
                    id="data-engineer",
                    preferred_label="Data Engineer",
                ),
                score=0.6,
                skill_gap=SkillGap(
                    missing_essential=[
                        SemanticEntity(
                            id="spark",
                            preferred_label="Spark",
                        ),
                    ],
                    total_essential=5,
                ),
            ),
        ],
    )

    explainer = CareerPathExplainer()

    explanation = explainer.explain(
        career_path,
    )

    assert explanation == CareerPathExplanation(
        summary=(
            "Data Analyst appears before Data Engineer "
            "because it is a stronger match."
        ),
        reasons=[
            "Data Analyst requires 2 additional essential skills.",
            "Data Engineer requires 1 additional essential skill.",
            "Data Analyst has a match score of 80%.",
            "Data Engineer has a match score of 60%.",
        ],
    )