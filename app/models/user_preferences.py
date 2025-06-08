from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

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