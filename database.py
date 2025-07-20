import os 
from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv 

load_dotenv() 

# MongoDB Atlas connection URI
uri = os.getenv("MONGODB_URI")

# Create a client and connect to the server
client = MongoClient(uri)

# Optional: Test connection (safe to remove in production)
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print("Connection failed:", e)

# Use database and collections
db = client["hrone_db"]
product_collection = db["products"]
order_collection = db["orders"]

