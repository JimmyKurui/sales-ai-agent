from pymongo import AsyncMongoClient, errors
from api.config import MONGODB_URI, MONGODB_NAME
mongodb_client = None
db = None

def connect_to_mongo():
    global mongodb_client, db
    mongodb_client = AsyncMongoClient(MONGODB_URI)
    db = mongodb_client.get_database(MONGODB_NAME)
    print("Connected to the MongoDB database!")

def close_mongo_connection():
    global mongodb_client
    if mongodb_client:
        mongodb_client.close()
        print('MongoDB connection closed!')

def check_db():
    global mongodb_client, db
    try:
        if mongodb_client:
            mongodb_client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
            
            collections = ["users", "messages", "leads", "personas"]
            
            try:
                for collection_name in list(set(collections) - set(db.list_collection_names()) ):
                        db.create_collection(collection_name)
                        print(f"Collection {collection_name} created successfully.")
            except errors.CollectionInvalid:
                print(f"Collection {collection_name} already exists.")
        else:
            print("MongoDB client is not initialized.")
    except Exception as e:
        print(e)
