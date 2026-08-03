from career_agent.models.candidate_profile import CandidateProfile


def create_candidate_profile(**kwargs) -> CandidateProfile:

    data = {
        "skills": [],
        "languages": [],
        "years_experience": 0,
        "salary": None,
        "preferred_remote_type": None,
        "preferred_countries": [],
    }

    data.update(kwargs)

    return CandidateProfile(**data)