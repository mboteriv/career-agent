from career_agent.models.semantic_entity import SemanticEntity
from career_agent.models.skill_gap import SkillGap


def test_essential_coverage_returns_one_when_no_skills_are_missing():

    gap = SkillGap(
        total_essential=4,
    )

    assert gap.essential_coverage == 1.0
    
def test_essential_coverage_returns_half():

    gap = SkillGap(
        total_essential=4,
        missing_essential=[
            SemanticEntity(
                id="1",
                preferred_label="A",
            ),
            SemanticEntity(
                id="2",
                preferred_label="B",
            ),
        ],
    )

    assert gap.essential_coverage == 0.5