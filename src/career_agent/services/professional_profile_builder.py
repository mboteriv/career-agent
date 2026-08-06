from career_agent.models.cv_extraction import (
    CVExtraction,
)
from career_agent.models.professional_profile import (
    ProfessionalProfile,
)



class ProfessionalProfileBuilder:
    
    def build(
        self,
        extraction: CVExtraction,
    ) -> ProfessionalProfile:

        return ProfessionalProfile(
            skills=extraction.skills,
            knowledge=extraction.education,
            languages=extraction.languages,
        )