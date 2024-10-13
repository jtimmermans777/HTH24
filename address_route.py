import webbrowser

def generate_google_maps_url(start_lat, start_lon, dest_lat, dest_lon):
    """
    Generate a Google Maps URL for driving directions.
    :param start_lat: Latitude of the user's starting location.
    :param start_lon: Longitude of the user's starting location.
    :param dest_lat: Latitude of the destination.
    :param dest_lon: Longitude of the destination.
    :return: URL string for Google Maps driving directions.
    """
    url = f"https://www.google.com/maps/dir/{start_lat},{start_lon}/{dest_lat},{dest_lon}/"
    return url

def open_google_maps(start_lat, start_lon, dest_lat, dest_lon):
    """
    Opens Google Maps in the browser with a route from the user's current location to the destination.
    :param start_lat: Latitude of the user's starting location.
    :param start_lon: Longitude of the user's starting location.
    :param dest_lat: Latitude of the destination.
    :param dest_lon: Longitude of the destination.
    """
    maps_url = generate_google_maps_url(start_lat, start_lon, dest_lat, dest_lon)
    webbrowser.open(maps_url)

# Example usage:
# User's current location (e.g., Boston, MA)
user_lat = 42.3601  # User's current latitude
user_lon = -71.0589  # User's current longitude

# Destination location (e.g., parking spot in Newton, MA)
dest_lat = 42.3371  # Destination latitude
dest_lon = -71.2092  # Destination longitude

# Open Google Maps with the route from user's location to the destination
open_google_maps(user_lat, user_lon, dest_lat, dest_lon)

