from career_agent.models.salary_expectation import (
    SalaryExpectation,
)
import pytest
from pydantic import ValidationError


def test_create_salary_expectation():

    salary = SalaryExpectation(
        amount=60000,
    )

    assert salary.amount == 60000
    assert salary.currency == "EUR"

def test_salary_expectation_is_immutable():

    salary = SalaryExpectation(
        amount=60000,
    )

    with pytest.raises(ValidationError):
        salary.amount = 70000