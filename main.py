from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
from bson import ObjectId

# Define response models for better Swagger documentation
class GenericItem(BaseModel):
    """
    Represents an item in the generic collection.
    Add fields based on your actual data structure.
    """
    id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    created_at: Optional[str] = None
    
    class Config:
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "id": "123",
                "name": "Sample Item",
                "description": "This is a sample item",
                "created_at": "2024-01-01T00:00:00"
            }
        }

class Settings(BaseModel):
    timezone: str = Field(default="UTC")
    location: str = Field(default="US")

class Preferences(BaseModel):
    theme: str = Field(default="dark")
    notifications_enabled: bool = Field(default=True)
    language: str = Field(default="en")

class UserPreferences(BaseModel):
    user_id: str
    preferences: Preferences
    settings: Settings

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }

class UserPreferencesUpdate(BaseModel):
    preferences: Optional[Preferences] = None
    settings: Optional[Settings] = None

app = FastAPI(
    title="ItsAMatch API",
    description="This API provides access to the ItsAMatch database.",
    version="1.0.0"
)

# MongoDB connection
MONGO_CONNECTION_STRING = "mongodb+srv://groupthreesailor:groupthree@cluster0.44c3nbp.mongodb.net/"
try:
    client = MongoClient(MONGO_CONNECTION_STRING)
    # Test the connection
    client.admin.command('ping')
except Exception as e:
    print(f"Failed to connect to MongoDB: {str(e)}")
    raise

# Define database and collection
db = client["ItsAMatch"]
collection = db["generic"]  # Using the generic collection for user preferences

@app.get("/",
    tags=["General"],
    summary="Root endpoint",
    description="Returns a welcome message"
)
async def root():
    return {"message": "Welcome to the ItsAMatch API"}

@app.post("/user/preferences/",
    tags=["User Preferences"],
    summary="Create user preferences",
    description="Create new user preferences",
    response_model=Dict[str, Any]
)
async def create_user_preferences(preferences: UserPreferences):
    try:
        # Check if user preferences already exist
        existing = collection.find_one({"user_id": preferences.user_id})
        if existing:
            raise HTTPException(
                status_code=400,
                detail=f"Preferences for user {preferences.user_id} already exist"
            )

        # Insert new preferences
        result = collection.insert_one(preferences.dict())
        
        # Return created document
        created = collection.find_one({"_id": result.inserted_id}, {"_id": 0})
        return created

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while creating preferences: {str(e)}"
        )

@app.get("/user/preferences/{user_id}",
    tags=["User Preferences"],
    summary="Get user preferences",
    description="Retrieve user preferences by user ID",
    response_model=Dict[str, Any]
)
async def get_user_preferences(user_id: str):
    try:
        preferences = collection.find_one({"user_id": user_id}, {"_id": 0})
        if not preferences:
            raise HTTPException(
                status_code=404,
                detail=f"No preferences found for user {user_id}"
            )
        return preferences

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while fetching preferences: {str(e)}"
        )

@app.put("/user/preferences/{user_id}",
    tags=["User Preferences"],
    summary="Update user preferences",
    description="Update user preferences by user ID",
    response_model=Dict[str, Any]
)
async def update_user_preferences(user_id: str, preferences: UserPreferencesUpdate):
    try:
        # Check if preferences exist
        existing = collection.find_one({"user_id": user_id})
        if not existing:
            raise HTTPException(
                status_code=404,
                detail=f"No preferences found for user {user_id}"
            )

        # Prepare update data
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

        # Update preferences
        result = collection.update_one(
            {"user_id": user_id},
            {"$set": update_data}
        )

        if result.modified_count == 0:
            raise HTTPException(
                status_code=400,
                detail="Update failed"
            )

        # Return updated document
        updated = collection.find_one({"user_id": user_id}, {"_id": 0})
        return updated

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while updating preferences: {str(e)}"
        )

@app.delete("/user/preferences/{user_id}",
    tags=["User Preferences"],
    summary="Delete user preferences",
    description="Delete user preferences by user ID",
    response_model=Dict[str, str]
)
async def delete_user_preferences(user_id: str):
    try:
        # Check if preferences exist
        existing = collection.find_one({"user_id": user_id})
        if not existing:
            raise HTTPException(
                status_code=404,
                detail=f"No preferences found for user {user_id}"
            )

        # Delete preferences
        result = collection.delete_one({"user_id": user_id})
        
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=400,
                detail="Delete failed"
            )

        return {"message": f"Preferences for user {user_id} deleted successfully"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while deleting preferences: {str(e)}"
        )

@app.get("/test-connection",
    tags=["System"],
    summary="Test MongoDB connection",
    description="Tests the connection to MongoDB and returns connection status"
)
async def test_connection():
    try:
        # Test connection
        db_status = db.command("serverStatus")
        
        # Get collection stats
        stats = db.command("collstats", "generic")
        
        return {
            "connection_string": MONGO_CONNECTION_STRING,
            "status": "Connected",
            "database": {
                "name": "ItsAMatch",
                "status": "Connected",
                "collection": "generic",
                "document_count": collection.count_documents({}),
                "size": stats.get("size", 0)
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"MongoDB connection error: {str(e)}"
        )

@app.get("/generic",
    tags=["Generic Items"],
    summary="Get all items",
    description="Retrieves all items from the generic collection in ItsAMatch database",
    response_model=List[Dict[str, Any]]
)
async def list_generic_items():
    try:
        items = list(collection.find({}, {"_id": 0}))
        return items
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while fetching items: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 