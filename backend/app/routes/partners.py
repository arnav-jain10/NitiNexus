from fastapi import APIRouter, Query
from app.database import SessionLocal
from app.models import ChannelPartner, Scheme

router = APIRouter(prefix="/partners", tags=["Partners"])


def serialize(partner):
    return {
        "partner_id": partner.partner_id,
        "name": partner.name,
        "type": partner.type,
        "state": partner.state,
        "district": partner.district,
        "address": partner.address,
        "contact_number": partner.contact_number,
        "email": partner.email,
        "navigation_link": partner.navigation_link,
        "supported_scheme_types": partner.supported_scheme_types,
        "supported_scheme_ids": partner.supported_scheme_ids,
        "active": bool(partner.active),
        "eligible_for_new_applications": bool(partner.eligible_for_new_applications),
    }


@router.get("/")
def get_partners(
    state: str | None = Query(default=None),
    district: str | None = Query(default=None),
    scheme_id: str | None = Query(default=None),
):
    db = SessionLocal()
    try:
        base = db.query(ChannelPartner).filter(ChannelPartner.active == True).all()
        scheme = db.query(Scheme).filter(Scheme.scheme_id == scheme_id).first() if scheme_id else None

        def scheme_matches(partner):
            if not scheme_id:
                return True
            ids = partner.supported_scheme_ids or []
            types = [str(x).lower() for x in (partner.supported_scheme_types or [])]
            return scheme_id in ids or (
                scheme is not None and (
                    str(scheme.type).lower() in types or
                    str(scheme.name).lower() in types
                )
            )

        candidates = [p for p in base if scheme_matches(p)]
        selected = candidates
        scope = "all available partners"
        scheme_support_verified = True

        if state:
            state_key = state.strip().lower()
            district_key = district.strip().lower() if district else ""
            state_matches = [p for p in candidates if (p.state or "").strip().lower() == state_key]
            if district:
                district_matches = [p for p in state_matches if (p.district or "").strip().lower() == district_key]
                if district_matches:
                    selected = district_matches
                    scope = "district"
                elif state_matches:
                    selected = state_matches
                    scope = "state"
                else:
                    selected = [p for p in candidates if (p.state or "").lower().startswith("multi-state")]
                    scope = "multi-state"
            elif state_matches:
                selected = state_matches
                scope = "state"
            else:
                selected = [p for p in candidates if (p.state or "").lower().startswith("multi-state")]
                scope = "multi-state"

            # Some directory records are general banking channels rather than
            # explicitly scheme-tagged. If no scheme-specific partner can be
            # found, show location partners as a transparent fallback instead
            # of returning an empty result. The UI labels these for verification.
            if not selected:
                location_base = base
                location_state = [p for p in location_base if (p.state or "").strip().lower() == state_key]
                if district:
                    location_district = [p for p in location_state if (p.district or "").strip().lower() == district_key]
                else:
                    location_district = []
                if location_district:
                    selected = location_district
                    scope = "district-location-fallback"
                elif location_state:
                    selected = location_state
                    scope = "state-location-fallback"
                else:
                    selected = [p for p in location_base if (p.state or "").lower().startswith("multi-state")]
                    scope = "multi-state-location-fallback"
                scheme_support_verified = False

        serialized = []
        for partner in selected:
            item = serialize(partner)
            item["scheme_support_verified"] = scheme_support_verified
            if not scheme_support_verified:
                item["scheme_support_note"] = "This partner is listed for your location, but scheme-specific support was not explicitly tagged in the directory. Confirm support before applying."
            serialized.append(item)

        return {
            "count": len(selected),
            "scope": scope,
            "scheme_support_verified": scheme_support_verified,
            "partners": serialized,
        }
    finally:
        db.close()
