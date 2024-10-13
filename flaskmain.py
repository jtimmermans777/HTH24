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
    {"_id": 0, "freeSpots": 5, "totalSpots": 11, "latitude": 41.36448, "longitude": -70.89319},
    {"_id": 1, "freeSpots": 17, "totalSpots": 23, "latitude": 42.27754, "longitude": -70.8787},
    {"_id": 2, "freeSpots": 16, "totalSpots": 24, "latitude": 42.08917, "longitude": -71.34238},
    {"_id": 3, "freeSpots": 23, "totalSpots": 30, "latitude": 42.06019, "longitude": -71.29891},
    {"_id": 4, "freeSpots": 8, "totalSpots": 10, "latitude": 42.36008, "longitude": -71.05888},
    {"_id": 5, "freeSpots": 10, "totalSpots": 15, "latitude": 42.34672, "longitude": -71.10435},
    {"_id": 6, "freeSpots": 20, "totalSpots": 25, "latitude": 42.36115, "longitude": -71.05708},
    {"_id": 7, "freeSpots": 14, "totalSpots": 18, "latitude": 42.34987, "longitude": -71.08457},
    {"_id": 8, "freeSpots": 12, "totalSpots": 20, "latitude": 42.35323, "longitude": -71.07228},
    {"_id": 9, "freeSpots": 19, "totalSpots": 22, "latitude": 42.36297, "longitude": -71.05774},
    {"_id": 10, "freeSpots": 8, "totalSpots": 12, "latitude": 42.33918, "longitude": -71.14985},
    {"_id": 11, "freeSpots": 9, "totalSpots": 13, "latitude": 42.35464, "longitude": -71.05549},
    {"_id": 12, "freeSpots": 6, "totalSpots": 10, "latitude": 42.35755, "longitude": -71.06247},
    {"_id": 13, "freeSpots": 10, "totalSpots": 15, "latitude": 42.36082, "longitude": -71.05484},
    {"_id": 14, "freeSpots": 11, "totalSpots": 14, "latitude": 42.34949, "longitude": -71.08033},
    {"_id": 15, "freeSpots": 7, "totalSpots": 10, "latitude": 42.34465, "longitude": -71.10134},
    {"_id": 16, "freeSpots": 5, "totalSpots": 8, "latitude": 42.35235, "longitude": -71.06871},
    {"_id": 17, "freeSpots": 9, "totalSpots": 14, "latitude": 42.34746, "longitude": -71.09028},
    {"_id": 18, "freeSpots": 13, "totalSpots": 17, "latitude": 42.35224, "longitude": -71.07122},
    {"_id": 19, "freeSpots": 16, "totalSpots": 20, "latitude": 42.35101, "longitude": -71.07587},
    {"_id": 20, "freeSpots": 18, "totalSpots": 22, "latitude": 42.34651, "longitude": -71.09269},
    {"_id": 21, "freeSpots": 12, "totalSpots": 18, "latitude": 42.35624, "longitude": -71.06093},
    {"_id": 22, "freeSpots": 8, "totalSpots": 12, "latitude": 42.36057, "longitude": -71.05412},
    {"_id": 23, "freeSpots": 9, "totalSpots": 12, "latitude": 42.35711, "longitude": -71.05867},
    {"_id": 24, "freeSpots": 11, "totalSpots": 16, "latitude": 42.35272, "longitude": -71.06429},
    {"_id": 25, "freeSpots": 10, "totalSpots": 13, "latitude": 42.35184, "longitude": -71.06395},
    {"_id": 26, "freeSpots": 14, "totalSpots": 20, "latitude": 42.36167, "longitude": -71.0573},
    {"_id": 27, "freeSpots": 17, "totalSpots": 25, "latitude": 42.35769, "longitude": -71.05354},
    {"_id": 28, "freeSpots": 13, "totalSpots": 17, "latitude": 42.35516, "longitude": -71.06502},
    {"_id": 29, "freeSpots": 20, "totalSpots": 28, "latitude": 42.36135, "longitude": -71.05901},
    {"_id": 30, "freeSpots": 15, "totalSpots": 19, "latitude": 42.36215, "longitude": -71.0612},
    {"_id": 31, "freeSpots": 12, "totalSpots": 16, "latitude": 42.35812, "longitude": -71.06021},
    {"_id": 32, "freeSpots": 9, "totalSpots": 12, "latitude": 42.36124, "longitude": -71.06057},
    {"_id": 33, "freeSpots": 7, "totalSpots": 10, "latitude": 42.36023, "longitude": -71.05378},
    {"_id": 34, "freeSpots": 14, "totalSpots": 18, "latitude": 42.35901, "longitude": -71.06442},
    {"_id": 35, "freeSpots": 18, "totalSpots": 22, "latitude": 42.35789, "longitude": -71.06898},
    {"_id": 36, "freeSpots": 10, "totalSpots": 15, "latitude": 42.35647, "longitude": -71.06273},
    {"_id": 37, "freeSpots": 8, "totalSpots": 11, "latitude": 42.35575, "longitude": -71.05635},
    {"_id": 38, "freeSpots": 12, "totalSpots": 18, "latitude": 42.35846, "longitude": -71.06624},
    {"_id": 39, "freeSpots": 16, "totalSpots": 21, "latitude": 42.35973, "longitude": -71.06198}
]
        closest_parking = None
        min_distance = float('inf')

        for parking in parking_data:
            if parking['freeSpots'] > 0:
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
