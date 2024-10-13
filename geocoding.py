import requests
import exifread as ef
import zipfile
import os

def _convert_to_degrees(value):
    """
    Helper function to convert the GPS coordinates stored in the EXIF to degrees in float format.
    :param value:
    :type value: exifread.utils.Ratio
    :rtype: float
    """
    d = float(value.values[0].num) / float(value.values[0].den)
    m = float(value.values[1].num) / float(value.values[1].den)
    s = float(value.values[2].num) / float(value.values[2].den)

    return d + (m / 60.0) + (s / 3600.0)

def get_GPS(filepath):
    with open(filepath, 'rb') as f:
        tags = ef.process_file(f)

        latitude = tags.get('GPS GPSLatitude')
        latitude_ref = tags.get('GPS GPSLatitudeRef')
        longitude = tags.get('GPS GPSLongitude')
        longitude_ref = tags.get('GPS GPSLongitudeRef')

        if latitude and longitude and latitude_ref and longitude_ref:
            # Convert latitude
            lat_value = _convert_to_degrees(latitude)
            if latitude_ref.values[0] != 'N':  # South coordinates are negative
                lat_value = -lat_value

            # Convert longitude
            lon_value = _convert_to_degrees(longitude)
            if longitude_ref.values[0] != 'E':  # West coordinates are negative
                lon_value = -lon_value

            return {'latitude': lat_value, 'longitude': lon_value}
        else:
            # Return None if GPS data is not available
            return None

image_path = r"C:\Users\12023\Downloads\extracted_images\images\GOPR0090_with_gps_1.JPG"

# Get GPS coordinates
gps_data = get_GPS(image_path)

# Check if GPS data was found
if gps_data:
    latitude, longitude = gps_data['latitude'], gps_data['longitude']
    print(f"Latitude: {latitude}, Longitude: {longitude}")
else:
    print("No GPS data found in the image.")
