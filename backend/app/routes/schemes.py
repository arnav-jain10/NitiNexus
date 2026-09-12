from fastapi import APIRouter
from app.database import SessionLocal
from app.models import Scheme

router = APIRouter(
    prefix="/schemes",
    tags=["Schemes"]
)


@router.get("/")
def get_schemes():
    db = SessionLocal()

    try:
        schemes = db.query(Scheme).all()

        return {
            "schemes": [
                {
                    "scheme_id": scheme.scheme_id,
                    "name": scheme.name,
                    "type": scheme.type,
                    "implementing_body": scheme.implementing_body,
                    "channel": scheme.channel,
                    "project_cost_max": scheme.project_cost_max,
                    "loan_min": scheme.loan_min,
                    "loan_max": scheme.loan_max,
                    "interest_rate_beneficiary_percent": scheme.interest_rate_beneficiary_percent,
                    "income_limit_annual": scheme.income_limit_annual,
                    "category_required": scheme.category_required,
                    "gender_requirement": scheme.gender_requirement,
                    "purpose": scheme.purpose,
                    "documents_required": scheme.documents_required or [],
                    "source_url": scheme.source_url,
                    "data_verified": scheme.data_verified,
                    "last_verified": scheme.last_verified
                }
                for scheme in schemes
            ]
        }

    finally:
        db.close()