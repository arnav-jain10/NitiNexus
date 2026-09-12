from typing import Any, Dict, List, Tuple


def get_value(value):
    if value is None or value == "":
        return None

    try:
        return float(str(value).replace(",", "").replace("₹", "").strip())
    except (TypeError, ValueError):
        return None


def normalize_text(value):
    return str(value or "").strip().lower()


def split_values(value):
    if not value:
        return []

    if isinstance(value, list):
        return [normalize_text(x) for x in value if x]

    return [
        normalize_text(x)
        for x in str(value).split(";")
        if normalize_text(x)
    ]


def purpose_matches(profile_purpose, scheme_purpose):
    user_purpose = normalize_text(profile_purpose)
    scheme_purposes = split_values(scheme_purpose)

    if not user_purpose or not scheme_purposes:
        return True

    # Business-related matching
    if "business" in user_purpose:
        for purpose in scheme_purposes:
            if (
                "business" in purpose
                or "income-generating" in purpose
                or "small-scale" in purpose
                or "micro" in purpose
            ):
                return True

    # Education-related matching
    if (
        "education" in user_purpose
        or "course" in user_purpose
        or "study" in user_purpose
    ):
        for purpose in scheme_purposes:
            if (
                "education" in purpose
                or "course" in purpose
                or "technical" in purpose
                or "professional" in purpose
            ):
                return True

    # Exact matching
    for purpose in scheme_purposes:
        if user_purpose == purpose:
            return True

    return False

def check_eligibility(
    profile: Dict[str, Any],
    scheme: Dict[str, Any]
) -> Tuple[bool, List[str], List[str]]:

    reasons = []
    failures = []

    # ---------------- Category ----------------

    category = normalize_text(profile.get("category"))
    categories = split_values(scheme.get("category_required"))

    if categories and category not in categories:
        failures.append(
            f"Category '{profile.get('category')}' is not supported by this scheme."
        )
    elif categories:
        reasons.append(
            f"Your category matches ({profile.get('category')})."
        )

    # ---------------- Income ----------------

    income = get_value(profile.get("income"))
    income_limit = get_value(scheme.get("income_limit_annual"))

    if income is not None and income_limit is not None:

        if income > income_limit:
            excess = income - income_limit

            failures.append(
                f"Income exceeds the scheme limit by ₹{excess:,.0f} "
                f"(limit: ₹{income_limit:,.0f})."
            )

        else:
            reasons.append(
                f"Your income is within the limit (≤ ₹{income_limit:,.0f})."
            )

    # ---------------- Age ----------------

    # Age is collected as profile information but is NOT used as an
    # eligibility filter because the current scheme dataset does not
    # publish a scheme-specific age requirement.

    # ---------------- Purpose ----------------

    user_purpose = profile.get("purpose")
    scheme_purpose = scheme.get("purpose")

    if scheme_purpose:

        if purpose_matches(user_purpose, scheme_purpose):

            reasons.append(
                f"Your purpose matches ({user_purpose})."
            )

        else:

            failures.append(
                f"Purpose mismatch: your purpose is '{user_purpose}'."
            )

    # ---------------- Requested Support Amount ----------------

    requested_amount = get_value(
        profile.get("requested_amount")
    )
    loan_min = get_value(scheme.get("loan_min"))
    loan_max = get_value(scheme.get("loan_max"))

    if requested_amount is not None and loan_min is not None:
        if requested_amount < loan_min:
            failures.append(
                f"Requested support is below the scheme minimum loan of ₹{loan_min:,.0f}."
            )
        else:
            reasons.append(
                f"Your requested support meets the minimum loan requirement (≥ ₹{loan_min:,.0f})."
            )

    if requested_amount is not None and loan_max is not None:

        if requested_amount > loan_max:
            failures.append(
                f"Requested support exceeds the scheme maximum loan by "
                f"₹{requested_amount - loan_max:,.0f} "
                f"(maximum: ₹{loan_max:,.0f})."
            )
        else:
            reasons.append(
                f"Your requested support fits the scheme maximum loan "
                f"(≤ ₹{loan_max:,.0f})."
            )

    return len(failures) == 0, reasons, failures


# ---------------------------------------------------------
# FIT SCORE
# ---------------------------------------------------------

def income_fit(profile, scheme):

    income = get_value(profile.get("income"))
    limit = get_value(scheme.get("income_limit_annual"))

    if income is None or limit is None or limit <= 0:
        return 0.5

    if income > limit:
        return 0.0

    return max(0.0, min(1.0, 1.0 - income / limit))


def purpose_fit(profile, scheme):

    if not scheme.get("purpose"):
        return 0.5

    return 1.0 if purpose_matches(
        profile.get("purpose"),
        scheme.get("purpose")
    ) else 0.0


def requested_amount_fit(profile, scheme):

    amount = get_value(
        profile.get("requested_amount")
    )
    minimum = get_value(scheme.get("loan_min"))
    maximum = get_value(scheme.get("loan_max"))

    if amount is None or maximum is None or maximum <= 0:
        return 0.5

    if minimum is not None and amount < minimum:
        return 0.0
    if amount > maximum:
        return 0.0

    return max(
        0.0,
        min(1.0, 1.0 - (amount / maximum) * 0.5)
    )


def calculate_fit_score(profile, scheme):

    score = (
        income_fit(profile, scheme) * 0.40
        + purpose_fit(profile, scheme) * 0.40
        + requested_amount_fit(profile, scheme) * 0.20
    )

    return round(score * 100, 2)


# ---------------------------------------------------------
# MAIN MATCHING FUNCTION
# ---------------------------------------------------------

def match_schemes(
    profile: Dict[str, Any],
    schemes: List[Dict[str, Any]],
    top_n: int = 3
):

    eligible = []
    ineligible = []

    for scheme in schemes:

        is_eligible, reasons, failures = check_eligibility(
            profile,
            scheme
        )

        # IMPORTANT:
        # Score ONLY eligible schemes.

        if is_eligible:

            score = calculate_fit_score(
                profile,
                scheme
            )

            eligible.append({
                "scheme_id": scheme.get("scheme_id"),
                "name": scheme.get("name"),
                "type": scheme.get("type"),
                "implementing_body": scheme.get("implementing_body"),
                "match_percent": score,
                "why_recommended": reasons,
                "loan_min": scheme.get("loan_min"),
                "loan_max": scheme.get("loan_max"),
                "interest_rate_beneficiary_percent":
                    scheme.get("interest_rate_beneficiary_percent"),
                "interest_rate_via_channel_percent":
                    scheme.get("interest_rate_via_channel_percent"),
                "tenure_years":
                    scheme.get("tenure_years_max"),
                "moratorium_months":
                    scheme.get("moratorium_months"),
                "repayment_frequency":
                    scheme.get("repayment_frequency"),
                "channel_requirement":
                    scheme.get("channel"),
                "documents_required":
                    scheme.get("documents_required") or [],
                "source_url":
                    scheme.get("source_url"),
                "data_verified":
                    scheme.get("data_verified", False),
                "last_verified":
                    scheme.get("last_verified")
            })

        else:

            ineligible.append({
                "scheme_id": scheme.get("scheme_id"),
                "name": scheme.get("name"),
                "type": scheme.get("type"),
                "eligible": False,
                "why_not_eligible": failures,
                "source_url": scheme.get("source_url"),
                "data_verified": scheme.get("data_verified", False),
                "last_verified": scheme.get("last_verified")
            })

    # Highest score first
    eligible.sort(
        key=lambda x: x["match_percent"],
        reverse=True
    )

    return {
        "top_matches": eligible[:top_n],
        "eligible_schemes": eligible,
        "ineligible_schemes": ineligible,
        "summary": {
            "total_schemes_checked": len(schemes),
            "eligible_count": len(eligible),
            "ineligible_count": len(ineligible)
        },
        "disclaimer": (
            "This is an intelligent scheme-discovery and matching assistant. "
            "Final approval remains with the authorized scheme/channel process."
        )
    }