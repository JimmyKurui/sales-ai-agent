import os
import certifi
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


ca = certifi.where()
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    SESSION_TYPE = 'filesystem'  # 'redis' for better scalability
    SESSION_PERMANENT = False
    MONGODB_URI = os.environ.get('MONGODB_URI') or 'mongodb://localhost:27017'
    MONGODB_NAME = os.environ.get('MONGODB_NAME') or 'sales_agent_db'
    IBM_API_KEY = os.environ.get('IBM_API_KEY')
    IBM_MODEL_ID = os.environ.get('IBM_MODEL_ID')
    
    mongo = MongoClient(MONGODB_URI, server_api=ServerApi('1'), tls=True, tlsAllowInvalidCertificates=True)
    db = mongo[MONGODB_NAME]

    def check_db(mongo=mongo):
        try:
            mongo.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)