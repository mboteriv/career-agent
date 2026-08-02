from career_agent.models.job_requirements import JobRequirements

def test_create_job_requirements():

    requirements = JobRequirements()

    assert requirements.skills == []
    assert requirements.languages == []
    assert requirements.years_experience is None