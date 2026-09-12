from pydantic import BaseModel, Field


class ProfileCreate(BaseModel):
    age: int = Field(..., gt=0, le=100)
    state: str
    district: str
    annual_income: float = Field(..., ge=0)
    requested_amount: float | None = Field(default=None, gt=0)
    category: str
    purpose: str
    business_education: str


class ProfileDetailsUpdate(BaseModel):
    purpose: str = Field(..., min_length=1)
    requested_amount: float = Field(..., gt=0)
    business_education: str = Field(default="")


class MatchRequest(BaseModel):
    profile_id: int


class EMIRequest(BaseModel):
    loan_amount: float = Field(..., gt=0)
    interest_rate: float = Field(..., ge=0)
    tenure_years: float = Field(..., gt=0)
