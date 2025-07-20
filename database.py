from pymongo.mongo_client import MongoClient

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
db = client["hrone_db"]  # You can name it anything; this will be created on first insert
product_collection = db["products"]
order_collection = db["orders"]

