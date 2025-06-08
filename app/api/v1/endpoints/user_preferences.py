from fastapi import APIRouter, Depends
from app.models.user_preferences import UserPreferences, UserPreferencesUpdate
from app.services.user_preferences import UserPreferencesService
from typing import Dict, Any

router = APIRouter()
service = UserPreferencesService()

@router.post("/", response_model=Dict[str, Any])
async def create_user_preferences(preferences: UserPreferences):
    """
    Create new user preferences.
    """
    return await service.create_preferences(preferences)

@router.get("/{user_id}", response_model=Dict[str, Any])
async def get_user_preferences(user_id: str):
    """
    Retrieve user preferences by user ID.
    """
    return await service.get_preferences(user_id)

@router.put("/{user_id}", response_model=Dict[str, Any])
async def update_user_preferences(user_id: str, preferences: UserPreferencesUpdate):
    """
    Update user preferences by user ID.
    """
    return await service.update_preferences(user_id, preferences)

@router.delete("/{user_id}", response_model=Dict[str, str])
async def delete_user_preferences(user_id: str):
    """
    Delete user preferences by user ID.
    """
    return await service.delete_preferences(user_id) 