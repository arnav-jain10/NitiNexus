from typing import Any, Dict, List


def _norm(value: Any) -> str:
    return str(value or "").strip().casefold()


SCHEME_PARTNER_ROUTING = {
    "SCH001": {
        "scheme_name": "Micro Finance Scheme",
        "categories": [
            "State Channelizing Agencies (SCAs)",
        ],
        "reason": "Micro Finance Scheme is routed through State Channelizing Agencies.",
    },
    "SCH002": {
        "scheme_name": "Term Loan",
        "categories": [
            "Public Sector Banks (PSBs)",
            "Regional Rural Banks (RRBs)",
            "Co-operative Banks",
        ],
        "reason": "Term Loan is routed to bank-type partners in the prototype.",
    },
    "SCH003": {
        "scheme_name": "Aajeevika Micro-Finance Yojana (AMY)",
        "categories": [
            "NBFC-MFIs",
        ],
        "reason": "AMY is routed through NBFC-MFIs.",
    },
    "SCH004": {
        "scheme_name": "Udyam Nidhi Yojana (UNY)",
        "categories": [
            "Cooperative Societies",
            "Co-operative Banks",
            "Small Finance Banks",
        ],
        "reason": "UNY is routed through cooperative and small finance channels.",
    },
    "SCH005": {
        "scheme_name": "Educational Loan Scheme",
        "categories": [],
        "reason": "Educational Loan Scheme partner category needs verification.",
    },
}


def get_partner_categories(scheme: Dict[str, Any]) -> Dict[str, Any]:

    scheme_id = str(scheme.get("scheme_id") or "").strip()

    explicit_channel = str(scheme.get("channel") or "").strip()

    if explicit_channel:
        channel_lower = explicit_channel.casefold()
        matched = []

        aliases = {
            "nbfc-mfi": "NBFC-MFIs",
            "nbfc-mfis": "NBFC-MFIs",
            "cooperative societies": "Cooperative Societies",
            "cooperative banks": "Co-operative Banks",
            "small finance banks": "Small Finance Banks",
            "sfb": "Small Finance Banks",
            "sca": "State Channelizing Agencies (SCAs)",
            "scas": "State Channelizing Agencies (SCAs)",
        }

        for key, official in aliases.items():
            if key in channel_lower and official not in matched:
                matched.append(official)

        if matched:
            return {
                "scheme_id": scheme_id,
                "scheme_name": scheme.get("name"),
                "partner_categories": matched,
                "routing_status": "ready",
                "reason": "Derived from the scheme's explicit channel field.",
            }

    rule = SCHEME_PARTNER_ROUTING.get(scheme_id)

    if rule and rule["categories"]:
        return {
            "scheme_id": scheme_id,
            "scheme_name": scheme.get("name") or rule["scheme_name"],
            "partner_categories": rule["categories"],
            "routing_status": "ready",
            "reason": rule["reason"],
        }

    return {
        "scheme_id": scheme_id,
        "scheme_name": scheme.get("name"),
        "partner_categories": [],
        "routing_status": "needs_verification",
        "reason": (
            "No verified channel category is available. "
            "Do not suggest a partner until the channel is verified."
        ),
    }


def _partner_is_usable(partner: Dict[str, Any]) -> bool:

    if partner.get("active") is False:
        return False

    if partner.get("eligible_for_new_applications") is False:
        return False

    status = _norm(partner.get("fund_utilization_status"))

    if status in {"high npa", "restricted", "npa"}:
        return False

    return True


def _location_match(
    partner: Dict[str, Any],
    state: str | None,
    district: str | None,
) -> int:

    if not state and not district:
        return 1

    p_state = _norm(partner.get("state"))
    p_district = _norm(partner.get("district"))

    q_state = _norm(state)
    q_district = _norm(district)

    if district and q_district and p_district == q_district:
        if not state or not q_state or p_state == q_state:
            return 3

    if state and q_state and p_state == q_state:
        return 2

    return 0


def find_partners(
    scheme: Dict[str, Any],
    partners: List[Dict[str, Any]],
    state: str | None = None,
    district: str | None = None,
    limit: int = 10,
) -> Dict[str, Any]:

    routing = get_partner_categories(scheme)

    if routing["routing_status"] != "ready":
        return {
            "status": "no_partner",
            "message": (
                "A suitable partner category could not be verified for this scheme. "
                "Please verify the official channel before suggesting a partner."
            ),
            "routing": routing,
            "partners": [],
        }

    wanted_categories = {
        _norm(x)
        for x in routing["partner_categories"]
    }

    # Database partner types use short names.
    # Ritu's routing logic uses official/full category names.
    partner_type_aliases = {
        "sca": "state channelizing agencies (scas)",
        "psb": "public sector banks (psbs)",
        "rrb": "regional rural banks (rrbs)",
        "cooperative bank": "co-operative banks",
        "cooperative society": "cooperative societies",
        "nbfc-mfi": "nbfc-mfis",
        "small finance bank": "small finance banks",
        "other agency & sidbi": "other agencies & sidbi",
    }

    results = []

    for partner in partners:

        if not _partner_is_usable(partner):
            continue

        p_type = _norm(partner.get("type"))

        supported_ids = {
            str(x).strip()
            for x in (partner.get("supported_scheme_ids") or [])
        }

        supported_types = {
            _norm(x)
            for x in (partner.get("supported_scheme_types") or [])
        }

        # Normal category-based routing.
        category_match = (
            partner_type_aliases.get(p_type, p_type)
            in wanted_categories
        )

        # Explicit scheme ID support gets priority.
        # Example: CP019 explicitly supports SCH002 Term Loan.
        explicit_scheme_match = (
            bool(supported_ids)
            and scheme.get("scheme_id") in supported_ids
        )

        category_ok = category_match or explicit_scheme_match

        scheme_ok = (
            not supported_ids
            or scheme.get("scheme_id") in supported_ids
        )

        type_ok = (
            not supported_types
            or _norm(scheme.get("type")) in supported_types
        )

        if not (category_ok and scheme_ok and type_ok):
            continue

        loc_score = _location_match(
            partner,
            state,
            district,
        )

        if (state or district) and loc_score == 0:
            continue

        results.append((loc_score, partner))

    results.sort(
        key=lambda item: (
            -item[0],
            str(item[1].get("name") or "").casefold(),
        )
    )

    selected = [
        p for _, p in results[:max(1, limit)]
    ]

    if not selected:
        return {
            "status": "no_partner",
            "message": (
                "No suitable authorized partner is available for the selected "
                "scheme and location."
            ),
            "routing": routing,
            "search": {
                "state": state,
                "district": district,
            },
            "partners": [],
        }

    return {
        "status": "success",
        "message": f"{len(selected)} suitable partner(s) found.",
        "routing": routing,
        "search": {
            "state": state,
            "district": district,
        },
        "partners": selected,
    }