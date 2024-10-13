import schedule
import mongostorage
from mongostorage import *

def refresh_parking():
    updated_parking_locations = [
        {"latitude": 42.3371, "longitude": -71.2092, "available_spots": 3, "total_capacity": 50},
        {"latitude": 42.3484, "longitude": -71.2000, "available_spots": 12, "total_capacity": 100},
        {"latitude": 42.3408, "longitude": -71.1949, "available_spots": 0, "total_capacity": 25},
    ]

    for spot in updated_parking_locations:
        location = {"latitude": spot["latitude"], "longitude": spot["longitude"]}
        update_parking_spot(location, spot["available_spots"], spot["total_capacity"])

    

# Schedule the task every 5 minutes
schedule.every(5).minutes.do(refresh_parking)

# Keep the program running to execute the scheduled tasks
while True:
    schedule.run_pending()
    time.sleep(1)