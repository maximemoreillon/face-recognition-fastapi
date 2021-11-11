from pymongo import MongoClient
import os

mongodb_url = os.getenv('MONGODB_URL','mongodb://localhost:27017/')
mongodb_db = os.getenv('MONGODB_DB','face_recognition')

client = MongoClient(mongodb_url)
db = client[mongodb_db]
