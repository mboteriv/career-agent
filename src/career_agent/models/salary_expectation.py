from pydantic import BaseModel, ConfigDict


class SalaryExpectation(BaseModel):

    model_config = ConfigDict(frozen=True)

    amount: int
    currency: str = "EUR"