from pymongo import AsyncMongoClient, errors
from api.config.settings import MONGODB_URI, MONGODB_NAME


mongodb_client = None
db = None

def connect_to_mongo():
    global mongodb_client, db
    mongodb_client = AsyncMongoClient(MONGODB_URI)
    db = mongodb_client.get_database(MONGODB_NAME)
    print("Connected to the MongoDB database!")

async def close_mongo_connection():
    global mongodb_client
    if mongodb_client:
        await mongodb_client.close()
        print('MongoDB connection closed!')

async def check_db():
    global mongodb_client, db
    try:
        if mongodb_client:
            await mongodb_client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
            
            collections = ["users", "messages", "leads", "personas"]
            db_collections = await db.list_collection_names()
            try:
                for collection_name in list(set(collections) - set(db_collections) ):
                        await db.create_collection(collection_name)
                        print(f"Collection {collection_name} created successfully.")
            except errors.CollectionInvalid:
                print(f"Collection {collection_name} already exists.")
        else:
            print("MongoDB client is not initialized.")
    except Exception as e:
        print(e)

async def get_db():
    global db
    if db is None:
        connect_to_mongo()
    return db