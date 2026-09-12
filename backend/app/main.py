from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.profile import router as profile_router
from app.routes.schemes import router as schemes_router
from app.routes.partners import router as partners_router
from app.routes.match import router as match_router
from app.routes.emi import router as emi_router
from app.database import Base, engine
from app import models
app = FastAPI(
    
    title="SIH26092 Scheme Matching API",
    description="Backend for AI-Driven Scheme Matching",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "SIH26092 Backend is running"
    }


app.include_router(profile_router)
app.include_router(schemes_router)
app.include_router(partners_router)
app.include_router(match_router)
app.include_router(emi_router)


@app.get("/health")
def health():
    return {"status": "ok"}
