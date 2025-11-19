from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from database import db, create_document, get_documents
import os

app = FastAPI(title="Fintech Waitlist API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class WaitlistLead(BaseModel):
    name: Optional[str] = Field(None, description="Full name")
    email: EmailStr = Field(..., description="Email address")
    source: Optional[str] = Field("landing", description="Signup source")


@app.get("/")
def root():
    return {"status": "ok", "service": "backend", "env_ready": bool(os.getenv("DATABASE_URL"))}


@app.get("/test")
def test_db():
    try:
        if db is None:
            raise Exception("DB not configured")
        # Ping by listing collections
        _ = db.list_collection_names()
        return {"ok": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/waitlist")
def join_waitlist(payload: WaitlistLead):
    try:
        lead_id = create_document("waitlistlead", payload)
        return {"id": lead_id, "message": "You're on the list!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/waitlist")
def list_waitlist(limit: int = 10):
    try:
        docs = get_documents("waitlistlead", limit=limit)
        # Make ObjectIds JSON-safe
        for d in docs:
            if "_id" in d:
                d["id"] = str(d.pop("_id"))
        return {"items": docs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
