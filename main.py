from fastapi import FastAPI, HTTPException, Body
from pymongo import MongoClient
from typing import Dict, Any
from datetime import datetime
from bson import ObjectId
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="ItsAMatch API",
    description="This API provides access to the ItsAMatch database.",
    version="1.0.0"
)

# Add CORS middleware with explicit configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD"],  # Explicitly list all allowed methods
    allow_headers=["*"],  # Allows all headers
    expose_headers=["*"],  # Expose all headers
    max_age=86400,  # Cache preflight requests for 24 hours
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
collection = db["user_preferences"]  # Using user_preferences collection for all preferences

@app.get("/",
    tags=["General"],
    summary="Root endpoint",
    description="Returns a welcome message"
)
async def root():
    return {"message": "Welcome to the ItsAMatch API"}

@app.post("/user/{user_id}/app/{app_id}/preferences",
    tags=["User Preferences"],
    summary="Create app preferences",
    description="Create new preferences for a specific app for a user. The request body will be stored as-is under the preferences field.",
    response_model=Dict[str, Any]
)
async def create_app_preferences(
    user_id: str, 
    app_id: str, 
    body: Dict[str, Any] = Body(...)  # Accept any JSON body
):
    try:
        # Check if preferences for this user and app already exist
        existing = collection.find_one({
            "user_id": user_id,
            "app_id": app_id
        })
        
        if existing:
            # If preferences exist, return 200 OK with existing preferences
            return {k: v for k, v in existing.items() if k != '_id'}

        # Create new document with metadata and raw body under preferences
        new_preferences = {
            "user_id": user_id,
            "app_id": app_id,
            "preferences": body,  # Store the entire request body under preferences
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }

        # Insert the document
        result = collection.insert_one(new_preferences)
        
        # Return created document
        created = collection.find_one({"_id": result.inserted_id})
        return {k: v for k, v in created.items() if k != '_id'}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while creating app preferences: {str(e)}"
        )

@app.get("/user/{user_id}/app/{app_id}/preferences",
    tags=["User Preferences"],
    summary="Get app-specific preferences",
    description="Retrieve preferences for a specific app for a user",
    response_model=Dict[str, Any]
)
async def get_app_preferences(user_id: str, app_id: str):
    try:
        preferences = collection.find_one({
            "user_id": user_id,
            "app_id": app_id
        }, {"_id": 0})
        
        if not preferences:
            raise HTTPException(
                status_code=404,
                detail=f"No preferences found for app {app_id} and user {user_id}"
            )
            
        return preferences

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while fetching app preferences: {str(e)}"
        )

@app.put("/user/{user_id}/app/{app_id}/preferences",
    tags=["User Preferences"],
    summary="Update or create app preferences",
    description="Update preferences for a specific app for a user. If preferences don't exist, creates them. The request body will be stored as-is under the preferences field.",
    response_model=Dict[str, Any]
)
async def update_app_preferences(
    user_id: str, 
    app_id: str, 
    body: Dict[str, Any] = Body(...)  # Accept any JSON body
):
    try:
        # Check if preferences exist
        existing = collection.find_one({
            "user_id": user_id,
            "app_id": app_id
        })
        
        # Prepare update data with metadata and raw body under preferences
        update_data = {
            "user_id": user_id,
            "app_id": app_id,
            "preferences": body,  # Store the entire request body under preferences
            "updated_at": datetime.utcnow().isoformat()
        }

        if not existing:
            # If document doesn't exist, create it with both created_at and updated_at
            update_data["created_at"] = update_data["updated_at"]
            
            # Insert new document
            result = collection.insert_one(update_data)
            
            # Return created document
            created = collection.find_one({"_id": result.inserted_id})
            return {k: v for k, v in created.items() if k != '_id'}
        else:
            # Update existing document
            result = collection.update_one(
                {
                    "user_id": user_id,
                    "app_id": app_id
                },
                {"$set": update_data}
            )

            if result.modified_count == 0:
                raise HTTPException(
                    status_code=400,
                    detail="Update failed"
                )

            # Return updated document
            updated = collection.find_one({
                "user_id": user_id,
                "app_id": app_id
            })
            return {k: v for k, v in updated.items() if k != '_id'}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while updating app preferences: {str(e)}"
        )

@app.delete("/user/{user_id}/app/{app_id}/preferences",
    tags=["User Preferences"],
    summary="Delete app preferences",
    description="Delete preferences for a specific app for a user",
    response_model=Dict[str, str]
)
async def delete_app_preferences(user_id: str, app_id: str):
    try:
        # Delete app preferences
        result = collection.delete_one({
            "user_id": user_id,
            "app_id": app_id
        })

        if result.deleted_count == 0:
            raise HTTPException(
                status_code=404,
                detail=f"No preferences found for app {app_id} and user {user_id}"
            )

        return {"message": f"Preferences for app {app_id} deleted successfully"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while deleting app preferences: {str(e)}"
        )

@app.get("/test-connection",
    tags=["System"],
    summary="Test MongoDB connection",
    description="Tests the connection to MongoDB and returns connection status"
)
async def test_connection():
    try:
        client.admin.command('ping')
        return {"status": "Connected to MongoDB successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to connect to MongoDB: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 