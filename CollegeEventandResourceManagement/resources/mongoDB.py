from pymongo.mongo_client import MongoClient
import os
from dotenv import load_dotenv
from pathlib import Path



load_dotenv(Path(__file__).resolve().parent.parent/'.env')

uri=os.getenv("MONGO_URI")
mongo_client = MongoClient(uri)
db=os.getenv("MONGO_DB")
mongo_db = mongo_client[db]
collections=os.getenv("MONGO_COLLECTION")
collection = mongo_db[collections]
