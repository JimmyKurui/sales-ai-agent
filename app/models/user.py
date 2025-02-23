from datetime import datetime, timezone
from app.config import Config 

SESSION_TIMEOUT = 2 # minutes

class User:
    collection = Config.db.users

    @staticmethod
    def create_user(email, type):
        client = {
            'email': email,
            'type': type,
            'created_at': datetime.now(timezone.utc)
        }
        result = User.collection.insert_one(client)
        client['_id'] = str(result.inserted_id)
        return client

    @staticmethod
    def get_by_email(email):
        return User.collection.find_one({'email': email})