from flask import Flask, request, render_template
import math

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('base.html')

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

@app.route('/find_parking', methods=['GET', 'POST'])
def find_parking():
    if request.method == 'POST':
        user_location = request.get_json()
        user_lat = user_location['latitude']
        user_lon = user_location['longitude']

        parking_data = [
            {"_id": 0, "freeSpots": 5, "totalSpots": 11, "latitude": 42.36448, "longitude": -70.89319},
            {"_id": 1, "freeSpots": 17, "totalSpots": 23, "latitude": 42.27754, "longitude": -70.8787},
            {"_id": 2, "freeSpots": 16, "totalSpots": 24, "latitude": 42.08917, "longitude": -71.34238},
            {"_id": 3, "freeSpots": 23, "totalSpots": 30, "latitude": 42.06019, "longitude": -71.29891},
            # Add more parking data as needed
        ]

        closest_parking = None
        min_distance = float('inf')

        for parking in parking_data:
            if parking['freeSpots'] > 0:  # Only consider parking with free spots
                distance = haversine(user_lat, user_lon, parking['latitude'], parking['longitude'])
                if distance < min_distance:
                    min_distance = distance
                    closest_parking = parking

        if closest_parking:
            return render_template('base.html', closest_parking=closest_parking, distance_km=round(min_distance, 2))
        else:
            return render_template('base.html', error='No parking lots available')
    else:
        return render_template('base.html')

if __name__ == '__main__':
    app.run(debug=True)
