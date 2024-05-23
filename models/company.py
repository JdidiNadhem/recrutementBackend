from pydantic import BaseModel, EmailStr
from typing import List, Optional
from beanie import Document,Link
from datetime import datetime

class jobOffer(Document):
    title: str
    description: str
    company_id: Optional[Link[Company]] # type: ignore
    created_at: datetime = datetime.utcnow()
    
    class Settings:
        collection= "job_offers"

class Company(Document):
    name: str
    logo: str
    jobOffer: List[Link[jobOffer]] = [] # type: ignore
    profile: str
    isAdmin: bool
    
    class Settings:
        collection= "company"
    

class Token(BaseModel):
    access_token: str
    token_type: str
