from fastapi import APIRouter, HTTPException
from app.database import SessionLocal
from app.models import Profile
from app.schemas import ProfileCreate, ProfileDetailsUpdate

router = APIRouter(prefix="/profile", tags=["Profile"])


def profile_response(profile):
    return {
        "profile_id": profile.id,
        "age": profile.age,
        "state": profile.state,
        "district": profile.district,
        "annual_income": profile.annual_income,
        "requested_amount": profile.requested_amount,
        "category": profile.category,
        "purpose": profile.purpose,
        "business_education": profile.business_education,
    }


@router.post("/")
def create_profile(profile: ProfileCreate):
    db = SessionLocal()
    try:
        new_profile = Profile(**profile.model_dump())
        db.add(new_profile)
        db.commit()
        db.refresh(new_profile)
        return {"message": "Profile saved successfully", **profile_response(new_profile)}
    finally:
        db.close()


@router.put("/{profile_id}/details")
def update_profile_details(profile_id: int, details: ProfileDetailsUpdate):
    db = SessionLocal()
    try:
        profile = db.query(Profile).filter(Profile.id == profile_id).first()
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")

        profile.purpose = details.purpose
        profile.requested_amount = details.requested_amount
        profile.business_education = details.business_education
        db.commit()
        db.refresh(profile)
        return {"message": "Profile requirements updated successfully", **profile_response(profile)}
    finally:
        db.close()


@router.get("/{profile_id}")
def get_profile(profile_id: int):
    db = SessionLocal()
    try:
        profile = db.query(Profile).filter(Profile.id == profile_id).first()
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")
        return profile_response(profile)
    finally:
        db.close()
