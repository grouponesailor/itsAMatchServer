from fastapi import APIRouter
from app.api.v1.endpoints import user_preferences

api_router = APIRouter()

api_router.include_router(
    user_preferences.router,
    prefix="/user/preferences",
    tags=["User Preferences"]
) 