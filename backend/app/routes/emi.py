from fastapi import APIRouter
from app.schemas import EMIRequest

router = APIRouter(prefix="/emi", tags=["EMI"])


@router.post("/")
def calculate_emi(request: EMIRequest):

    principal = request.loan_amount
    annual_rate = request.interest_rate
    tenure_years = request.tenure_years

    monthly_rate = annual_rate / 12 / 100
    total_months = tenure_years * 12

    # Special case: 0% interest
    if monthly_rate == 0:
        emi = principal / total_months
    else:
        emi = (
            principal
            * monthly_rate
            * (1 + monthly_rate) ** total_months
            / ((1 + monthly_rate) ** total_months - 1)
        )

    total_payable = emi * total_months
    total_interest = total_payable - principal

    return {
        "loan_amount": principal,
        "interest_rate": annual_rate,
        "tenure_years": tenure_years,
        "tenure_months": total_months,
        "monthly_emi": round(emi, 2),
        "total_interest": round(total_interest, 2),
        "total_payable": round(total_payable, 2)
    }