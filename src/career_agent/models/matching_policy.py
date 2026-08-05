from pydantic import BaseModel
from pydantic import ConfigDict

from career_agent.models.matching_criterion import MatchingCriterion


class MatchingPolicy(BaseModel):

    model_config = ConfigDict(
        frozen=True,
    )

    skills_weight: float = 4.0
    experience_weight: float = 3.0
    languages_weight: float = 2.0
    salary_weight: float = 1.0
    remote_weight: float = 1.0
    country_weight: float = 1.0
    
    required_criteria: frozenset[
        MatchingCriterion
    ] = frozenset()
    
    def weight_for(
        self,
        criterion: MatchingCriterion,
    ) -> float:

        weights = {
            MatchingCriterion.SKILLS:
                self.skills_weight,

            MatchingCriterion.EXPERIENCE:
                self.experience_weight,

            MatchingCriterion.LANGUAGES:
                self.languages_weight,

            MatchingCriterion.SALARY:
                self.salary_weight,

            MatchingCriterion.REMOTE:
                self.remote_weight,

            MatchingCriterion.COUNTRY:
                self.country_weight,
        }

        return weights[
            criterion
        ]