from fastapi import HTTPException
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorClient

from models.user import Utilisateur, Token
from dotenv import dotenv_values

# Load environment variables
config = dotenv_values()

# Define password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Function to generate JWT token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config['SECRET_KEY'], algorithm=config['ALGORITHM'])
    return encoded_jwt

# MongoDB connection
client = AsyncIOMotorClient(config['MONGODB_URI'])
db = client[config['MONGODB_DB']]

async def login(utilisateur: Utilisateur):
    try:
        # Find user in the database
        user = await db["Utilisateur"].find_one({"email": utilisateur.email})
        
        # Check if user exists
        if user is None:
            raise HTTPException(status_code=400, detail="Invalid email or password")
        
        user["_id"] = str(user["_id"])
        
        # Verify password
        if not verify_password(utilisateur.password, user["password"]):
            raise HTTPException(status_code=400, detail="Invalid email or password")

        # Create JWT token
        access_token_expires = timedelta(minutes=15)
        access_token = create_access_token(
            data={"sub": user["email"]}, expires_delta=access_token_expires
        )

        return {"message": "Authentication successful", "user": user, "token": access_token}
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

async def register_user(user: Utilisateur):
    try:
        # Check if user with the same email already exists
        existing_user = await db["Utilisateur"].find_one({"email": user.email})
        if existing_user:
            raise HTTPException(status_code=400, detail="User with this email already exists")

        # Hash the password before storing it
        hashed_password = pwd_context.hash(user.password)

        # Insert new user into the database
        result = await db["Utilisateur"].insert_one({
            "email": user.email,
            "password": hashed_password,
            "role": user.role,
            "profile": user.profile,
            # Add additional fields as needed
        })

        # Check if insertion was successful
        if result.acknowledged:
            return {"message": "User registered successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to register user")
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to register user: {str(e)}")
