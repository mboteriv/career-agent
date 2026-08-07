from career_agent.models.occupation_match import OccupationMatch
from career_agent.models.semantic_entity import SemanticEntity
from career_agent.models.skill_gap import SkillGap
from career_agent.services.skill_gap_analyzer import (
    SkillGapAnalyzer,
)


class OccupationMatcher:

    def __init__(
        self,
        analyzer: SkillGapAnalyzer,
    ):
        self._analyzer = analyzer
        
    def match(
        self,
        occupation_id: str,
        candidate_skills: list[str],
    ) -> OccupationMatch:

        gap = self._analyzer.analyze(
            occupation_id,
            candidate_skills,
        )

        occupation = self._analyzer._repository.find_occupation_by_id(
            occupation_id,
        )

        return OccupationMatch(
            occupation=occupation,
            score=gap.essential_coverage,
            skill_gap=gap,
        )