from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class WaitlistLead(BaseModel):
    name: Optional[str] = Field(None, description="Full name")
    email: EmailStr = Field(..., description="Email address")
    source: Optional[str] = Field("landing", description="Signup source")
