from fastapi import FastAPI
from fastapi.routing import APIRouter
# from typing import Optional

from controllers.user import login, register_user
from models.user import Utilisateur,readUtilisateur

# Define your FastAPI app instance
app = FastAPI()

# Define your router
router = APIRouter()


@router.post("/api/user/login")
async def user_login(utilisateur: readUtilisateur):
    return await login(utilisateur)

@router.post("/api/user/register")
async def user_register(utilisateur: Utilisateur):
    return await register_user(utilisateur)


# Include your router in the FastAPI app
app.include_router(router)
