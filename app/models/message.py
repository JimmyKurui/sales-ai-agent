from datetime import datetime, timezone
from bson import ObjectId
from ..config import Config

def get_next_conversation_id():
    last_convo = Config.db.messages.find_one({}, {"conversation_id": 1}, sort=[("conversation_id", -1)])
    return (last_convo["conversation_id"] + 1) if last_convo else 1

class Message:

    collection = Config.db.messages

    @staticmethod
    def create(email, content, sender_type):
        message = {
            'email': email,
            'content': content,
            'sender_type': sender_type,
            'conversation_id': get_next_conversation_id(),
            'timestamp': datetime.now(timezone.utc),
        }
        result = Message.collection.insert_one(message)
        message['_id'] = str(result.inserted_id)
        return message

    @staticmethod
    def get_conversation(conversation_id, limit=50):
        messages = Message.collection.find(
            {'conversation_id': conversation_id}
        ).sort('timestamp', -1).limit(limit)
        return list(messages)