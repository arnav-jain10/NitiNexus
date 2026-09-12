from fastapi import APIRouter, HTTPException

from app.database import SessionLocal
from app.models import Profile, Scheme, MatchResult
from app.schemas import MatchRequest
from app.matching_engine import match_schemes as run_matching_engine


router = APIRouter(
    prefix="/match",
    tags=["Matching"]
)


@router.post("/")
def match_schemes(request: MatchRequest):

    db = SessionLocal()

    try:
        # ---------------------------------
        # GET PROFILE
        # ---------------------------------

        profile = db.query(Profile).filter(
            Profile.id == request.profile_id
        ).first()

        if not profile:
            raise HTTPException(
                status_code=404,
                detail="Profile not found"
            )

        # ---------------------------------
        # GET ALL SCHEMES
        # ---------------------------------

        schemes = db.query(Scheme).all()

        # ---------------------------------
        # CONVERT DATABASE OBJECTS
        # TO RITU ENGINE FORMAT
        # ---------------------------------

        profile_data = {
            "category": profile.category,
            "income": profile.annual_income,
            "state": profile.state,
            "district": profile.district,
            "purpose": profile.purpose,
            "requested_amount": profile.requested_amount
        }

        scheme_data = []

        for scheme in schemes:

            hard_filters = scheme.hard_filters or {}

            scheme_data.append({
                "scheme_id": scheme.scheme_id,
                "name": scheme.name,
                "type": scheme.type,
                "implementing_body": scheme.implementing_body,
                "channel": scheme.channel,
                "project_cost_max": scheme.project_cost_max,
                "loan_min": scheme.loan_min,
                "loan_max": scheme.loan_max,
                "financing_percent_of_project":
                    scheme.financing_percent_of_project,
                "interest_rate_beneficiary_percent":
                    scheme.interest_rate_beneficiary_percent,
                "interest_rate_via_channel_percent":
                    scheme.interest_rate_via_channel_percent,
                "tenure_years_max":
                    scheme.tenure_years_max,
                "moratorium_months":
                    scheme.moratorium_months,
                "repayment_frequency":
                    scheme.repayment_frequency,
                "income_limit_annual":
                    scheme.income_limit_annual,
                "category_required":
                    scheme.category_required,
                "gender_requirement":
                    scheme.gender_requirement,
                "purpose":
                    scheme.purpose,
                "documents_required":
                    scheme.documents_required or [],
                "source_url":
                    scheme.source_url,
                "data_verified":
                    scheme.data_verified,
                "last_verified":
                    scheme.last_verified,
                "hard_filters":
                    hard_filters
            })

        # ---------------------------------
        # RUN RITU'S MATCHING ENGINE
        # ---------------------------------

        result = run_matching_engine(
            profile_data,
            scheme_data,
            top_n=3
        )

        # ---------------------------------
        # SAVE ELIGIBLE MATCHES
        # ---------------------------------

        for matched in result["eligible_schemes"]:

            existing_result = db.query(MatchResult).filter(
                MatchResult.profile_id == profile.id,
                MatchResult.scheme_id == matched["scheme_id"]
            ).first()

            explanation = " ".join(
                matched.get("why_recommended", [])
            )

            if existing_result:

                existing_result.score = matched["match_percent"]
                existing_result.explanation = explanation

            else:

                new_result = MatchResult(
                    profile_id=profile.id,
                    scheme_id=matched["scheme_id"],
                    score=matched["match_percent"],
                    explanation=explanation
                )

                db.add(new_result)

        db.commit()

        # ---------------------------------
        # FINAL API RESPONSE
        # ---------------------------------

        return {
            "profile_id": profile.id,
            "total_schemes_checked":
                result["summary"]["total_schemes_checked"],
            "eligible_count":
                result["summary"]["eligible_count"],
            "ineligible_count":
                result["summary"]["ineligible_count"],
            "top_matches":
                result["top_matches"],
            "eligible_schemes":
                result["eligible_schemes"],
            "ineligible_schemes":
                result["ineligible_schemes"],
            "disclaimer":
                result["disclaimer"]
        }

    finally:
        db.close()