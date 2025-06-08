from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from app.core.config import settings
import logging

try:
    client = MongoClient(settings.MONGODB_URL, 
                        serverSelectionTimeoutMS=5000,  # 5 second timeout
                        connectTimeoutMS=5000)
    # Force a connection attempt
    client.admin.command('ping')
    db = client[settings.DATABASE_NAME]
    collection = db[settings.COLLECTION_NAME]
    logging.info("Successfully connected to MongoDB.")
except ConnectionFailure as e:
    logging.error(f"Could not connect to MongoDB: {e}")
    raise

def get_collection():
    return collection 