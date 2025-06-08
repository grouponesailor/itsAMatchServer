from pymongo import MongoClient

# MongoDB connection
MONGO_CONNECTION_STRING = "mongodb+srv://groupthreesailor:groupthree@cluster0.44c3nbp.mongodb.net/"
client = MongoClient(MONGO_CONNECTION_STRING)
db = client["ItsAMatch"]
collection = db["generic"]  # Using the generic collection for user preferences

# Test data
test_users = [
    {
        "user_id": "user1",
        "preferences": {
            "theme": "dark",
            "notifications_enabled": True,
            "language": "en"
        },
        "settings": {
            "timezone": "UTC",
            "location": "US"
        }
    },
    {
        "user_id": "user2",
        "preferences": {
            "theme": "light",
            "notifications_enabled": False,
            "language": "es"
        },
        "settings": {
            "timezone": "Europe/Madrid",
            "location": "ES"
        }
    },
    {
        "user_id": "user3",
        "preferences": {
            "theme": "system",
            "notifications_enabled": True,
            "language": "fr"
        },
        "settings": {
            "timezone": "Europe/Paris",
            "location": "FR"
        }
    },
    {
        "user_id": "user4",
        "preferences": {
            "theme": "dark",
            "notifications_enabled": True,
            "language": "de"
        },
        "settings": {
            "timezone": "Europe/Berlin",
            "location": "DE"
        }
    },
    {
        "user_id": "user5",
        "preferences": {
            "theme": "light",
            "notifications_enabled": False,
            "language": "it"
        },
        "settings": {
            "timezone": "Europe/Rome",
            "location": "IT"
        }
    }
]

def insert_test_data():
    try:
        # Clear existing data
        collection.delete_many({})
        
        # Insert test data
        result = collection.insert_many(test_users)
        
        print(f"Successfully inserted {len(result.inserted_ids)} test users")
        
        # Verify the data
        for user in test_users:
            user_id = user["user_id"]
            found_user = collection.find_one({"user_id": user_id}, {"_id": 0})
            print(f"\nVerified user {user_id}:")
            print(found_user)
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    insert_test_data() 