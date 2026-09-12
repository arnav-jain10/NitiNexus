from fastapi import APIRouter
from app.database import SessionLocal
from app.models import ChannelPartner

router = APIRouter(
    prefix="/partners",
    tags=["Partners"]
)


@router.get("/")
def get_partners():
    db = SessionLocal()

    try:
        partners = db.query(ChannelPartner).all()

        return {
            "partners": [
                {
                    "partner_id": partner.partner_id,
                    "name": partner.name,
                    "type": partner.type,
                    "state": partner.state,
                    "district": partner.district,
                    "address": partner.address,
                    "contact_number": partner.contact_number,
                    "email": partner.email,
                    "navigation_link": partner.navigation_link,
                    "active": partner.active,
                    "fund_utilization_status": partner.fund_utilization_status,
                    "npa_percentage": partner.npa_percentage,
                    "eligible_for_new_applications": partner.eligible_for_new_applications
                }
                for partner in partners
            ]
        }

    finally:
        db.close()