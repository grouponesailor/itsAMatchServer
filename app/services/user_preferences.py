from fastapi import HTTPException
from app.core.database import get_collection
from app.models.user_preferences import UserPreferences, UserPreferencesUpdate
from typing import Dict, Any

class UserPreferencesService:
    def __init__(self):
        self.collection = get_collection()

    async def create_preferences(self, preferences: UserPreferences) -> Dict[str, Any]:
        existing = self.collection.find_one({"user_id": preferences.user_id})
        if existing:
            raise HTTPException(
                status_code=400,
                detail=f"Preferences for user {preferences.user_id} already exist"
            )

        result = self.collection.insert_one(preferences.dict())
        created = self.collection.find_one({"_id": result.inserted_id}, {"_id": 0})
        return created

    async def get_preferences(self, user_id: str) -> Dict[str, Any]:
        preferences = self.collection.find_one({"user_id": user_id}, {"_id": 0})
        if not preferences:
            raise HTTPException(
                status_code=404,
                detail=f"No preferences found for user {user_id}"
            )
        return preferences

    async def update_preferences(self, user_id: str, preferences: UserPreferencesUpdate) -> Dict[str, Any]:
        existing = self.collection.find_one({"user_id": user_id})
        if not existing:
            raise HTTPException(
                status_code=404,
                detail=f"No preferences found for user {user_id}"
            )

        update_data = {}
        if preferences.preferences:
            update_data["preferences"] = preferences.preferences.dict()
        if preferences.settings:
            update_data["settings"] = preferences.settings.dict()

        if not update_data:
            raise HTTPException(
                status_code=400,
                detail="No update data provided"
            )

        result = self.collection.update_one(
            {"user_id": user_id},
            {"$set": update_data}
        )

        if result.modified_count == 0:
            raise HTTPException(
                status_code=400,
                detail="Update failed"
            )

        updated = self.collection.find_one({"user_id": user_id}, {"_id": 0})
        return updated

    async def delete_preferences(self, user_id: str) -> Dict[str, str]:
        existing = self.collection.find_one({"user_id": user_id})
        if not existing:
            raise HTTPException(
                status_code=404,
                detail=f"No preferences found for user {user_id}"
            )

        result = self.collection.delete_one({"user_id": user_id})
        
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=400,
                detail="Delete failed"
            )

        return {"message": f"Preferences for user {user_id} deleted successfully"} 