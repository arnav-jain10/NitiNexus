from fastapi import APIRouter, HTTPException
from app.database import SessionLocal
from app.models import Profile, Scheme, MatchResult
from app.schemas import MatchRequest

router = APIRouter(
    prefix="/match",
    tags=["Matching"]
)


@router.post("/")
def match_schemes(request: MatchRequest):
    db = SessionLocal()

    try:
        profile = db.query(Profile).filter(
            Profile.id == request.profile_id
        ).first()

        if not profile:
            raise HTTPException(
                status_code=404,
                detail="Profile not found"
            )

        schemes = db.query(Scheme).all()

        matched_schemes = []

        for scheme in schemes:

            filters = scheme.hard_filters or {}

            # -----------------------------
            # HARD ELIGIBILITY CHECKS
            # -----------------------------

            required_categories = filters.get(
                "category_required", []
            )

            if (
                required_categories
                and profile.category not in required_categories
            ):
                continue

            income_max = filters.get("income_max")

            if (
                income_max is not None
                and profile.annual_income > income_max
            ):
                continue

            age_min = filters.get("age_min")

            if (
                age_min is not None
                and profile.age < age_min
            ):
                continue

            age_max = filters.get("age_max")

            if (
                age_max is not None
                and profile.age > age_max
            ):
                continue

            # -----------------------------
            # PURPOSE MATCHING
            # -----------------------------

            user_purpose = profile.purpose.lower().strip()

            scheme_purposes = [
                str(purpose).lower()
                for purpose in (scheme.purpose or [])
            ]

            purpose_score = 0
            purpose_reason = "Purpose does not strongly match"

            # Business purpose
            if "business" in user_purpose:

                if any(
                    "business setup" in purpose
                    or "business expansion" in purpose
                    for purpose in scheme_purposes
                ):
                    purpose_score = 30
                    purpose_reason = (
                        "Very strong purpose match: "
                        "business setup or expansion"
                    )

                elif any(
                    "small/micro business" in purpose
                    for purpose in scheme_purposes
                ):
                    purpose_score = 25
                    purpose_reason = (
                        "Strong purpose match: "
                        "small or micro business"
                    )

                elif any(
                    "income-generating" in purpose
                    for purpose in scheme_purposes
                ):
                    purpose_score = 20
                    purpose_reason = (
                        "Good purpose match: "
                        "income-generating activity"
                    )

                else:
                    continue

            # Education purpose
            elif (
                "education" in user_purpose
                or "course" in user_purpose
                or "study" in user_purpose
            ):

                if any(
                    "course" in purpose
                    for purpose in scheme_purposes
                ):
                    purpose_score = 30
                    purpose_reason = (
                        "Very strong purpose match: "
                        "professional or technical course"
                    )
                else:
                    continue

            # Other purposes
            else:

                for purpose in scheme_purposes:

                    words = purpose.split()

                    if any(
                        word in user_purpose
                        for word in words
                    ):
                        purpose_score = 20
                        purpose_reason = "Partial purpose match"
                        break

                if purpose_score == 0:
                    continue
            # -----------------------------
            # FINAL SCORE
            # -----------------------------

            score = 50 + purpose_score

            explanation = (
                "Passed hard eligibility checks for "
                "age, income and category. "
                + purpose_reason
            )

            # -----------------------------
            # SAVE MATCH RESULT
            # -----------------------------

            existing_result = db.query(MatchResult).filter(
                MatchResult.profile_id == profile.id,
                MatchResult.scheme_id == scheme.scheme_id
            ).first()

            if existing_result:
                existing_result.score = score
                existing_result.explanation = explanation
            else:
                result = MatchResult(
                    profile_id=profile.id,
                    scheme_id=scheme.scheme_id,
                    score=score,
                    explanation=explanation
                )

                db.add(result)

            matched_schemes.append({
                "scheme_id": scheme.scheme_id,
                "name": scheme.name,
                "type": scheme.type,
                "score": score,
                "reason": explanation,
                "loan_max": scheme.loan_max,
                "interest_rate_beneficiary_percent":
                    scheme.interest_rate_beneficiary_percent,
                "tenure_years_max": scheme.tenure_years_max,
                "documents_required": scheme.documents_required,
                "source_url": scheme.source_url
            })

        db.commit()

        matched_schemes.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        return {
            "profile_id": profile.id,
            "total_matches": len(matched_schemes),
            "matched_schemes": matched_schemes
        }

    finally:
        db.close()