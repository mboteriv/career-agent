from career_agent.repositories.semantic_repository import (
    SemanticRepository,
)
from career_agent.services.occupation_matcher import (
    OccupationMatcher,
)
from career_agent.models.career_path import (
    CareerPath,
)


class CareerPathExplorer:

    def __init__(
        self,
        repository: SemanticRepository,
        matcher: OccupationMatcher,
    ):
        self._repository = repository
        self._matcher = matcher
    
    def explore(
        self,
        candidate_skills: list[str],
        limit: int | None = None,
    ) -> CareerPath:

        occupations = []

        for occupation in self._repository.find_all_occupations():

            occupations.append(
                self._matcher.match(
                    occupation.id,
                    candidate_skills,
                ),
            )
        occupations.sort(
            key=lambda match: match.score,
            reverse=True,
        )
        if limit is not None:

            occupations = occupations[:limit]

        return CareerPath(
            occupations=occupations,
        )