from pymongo import MongoClient
from dotenv import load_dotenv
import os
import ssl

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

client = MongoClient(
    MONGO_URI,
    tls=True,
    tlsAllowInvalidCertificates=True, 
    serverSelectionTimeoutMS=30000
)

db = client[MONGO_DB]
sales_data = db["sales_data"]

def get_database():
    return db