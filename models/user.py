from pydantic import BaseModel, EmailStr

class readUtilisateur(BaseModel):
    email: EmailStr
    password: str

class Utilisateur(BaseModel):
    email: EmailStr
    password: str
    role: str
    profile: str
    

class Token(BaseModel):
    access_token: str
    token_type: str
