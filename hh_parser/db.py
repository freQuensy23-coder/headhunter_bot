from pymongo.mongo_client import MongoClient
from config import mongodb_database_string

uri = mongodb_database_string
# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection

client.admin.command('ping')
print("Pinged your deployment. You successfully connected to MongoDB!")
