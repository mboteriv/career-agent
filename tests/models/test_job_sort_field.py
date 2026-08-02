from career_agent.models.job_sort_field import JobSortField

def test_job_sort_field_values():

    assert JobSortField.CREATED_AT.value == "created_at"
    assert JobSortField.COMPANY_NAME.value == "company_name"
    assert JobSortField.TITLE.value == "title"