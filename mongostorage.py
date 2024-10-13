import pymongo
from pymongo import MongoClient
import time
from datetime import datetime
import os

# Connect to MongoDB
mongodb_uri = os.getenv("MONGODB_URI")
client = MongoClient('mongodb+srv://nuhinsalamun7:K8uCMdc3yobUquQu@parkingspot.htqfr.mongodb.net/')  # Change to your MongoDB URL if needed

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


db = client['parking_db']
collection = db['parking_spots']

def calculate_status(available_spots, total_capacity):
    """
    Determine the status of the parking location based on available spots and total capacity.
    """
    if available_spots == 0:
        return "Full"
    elif available_spots / total_capacity <= 0.1:  # Less than 10% available
        return "Almost Full"
    else:
        return "Not Full"

def update_parking_spot(location, available_spots, total_capacity):
    """
    Insert or update the parking spot data into MongoDB.
    """
    status = calculate_status(available_spots, total_capacity)
    last_updated = datetime.now()

    # Define the query and the update
    query = {"location": location}
    update = {
        "$set": {
            "availability": {
                "available_spots": available_spots,
                "total_capacity": total_capacity
            },
            "status": status,
            "last_updated": last_updated
        }
    }

    # Upsert: Update the document if it exists, otherwise insert a new one
    collection.update_one(query, update, upsert=True)

# Example of updating multiple parking spots
parking_locations = [
    {"latitude": 42.3371, "longitude": -71.2092, "available_spots": 5, "total_capacity": 50},
    {"latitude": 42.3484, "longitude": -71.2000, "available_spots": 15, "total_capacity": 100},
    {"latitude": 42.3408, "longitude": -71.1949, "available_spots": 0, "total_capacity": 25},
]

for spot in parking_locations:
    location = {"latitude": spot["latitude"], "longitude": spot["longitude"]}
    update_parking_spot(location, spot["available_spots"], spot["total_capacity"])


documents = collection.find()

# Iterate over and print each document
for document in documents:
    print(document)