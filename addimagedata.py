import piexif
import piexif.helper
import exifread

def convert_to_dms(value, is_latitude):
    """
    Convert decimal degrees to degrees, minutes, seconds (DMS) format.
    :param value: GPS coordinates in decimal degrees (e.g., 42.3371 or -71.2092).
    :param is_latitude: True if latitude, False if longitude.
    :return: tuple of degrees, minutes, and seconds in EXIF format.
    """
    degrees = int(abs(value))
    minutes = int((abs(value) - degrees) * 60)
    seconds = int(((abs(value) - degrees) * 60 - minutes) * 60 * 100)

    if is_latitude:
        direction = 'N' if value >= 0 else 'S'
    else:
        direction = 'E' if value >= 0 else 'W'

    return ((degrees, 1), (minutes, 1), (seconds, 100)), direction

def add_gps_metadata(image_path, output_path, lat, lon):
    """
    Adds fake GPS data to the EXIF metadata of an image without using Pillow.
    :param image_path: Path to the input image.
    :param output_path: Path to the output image with added EXIF metadata.
    :param lat: Latitude in decimal degrees.
    :param lon: Longitude in decimal degrees.
    """
    # Load existing EXIF data from the image
    exif_dict = piexif.load(image_path)

    # Convert latitude and longitude to DMS format
    lat_dms, lat_ref = convert_to_dms(lat, is_latitude=True)
    lon_dms, lon_ref = convert_to_dms(lon, is_latitude=False)

    # Create GPS IFD (Image File Directory) for EXIF
    gps_ifd = {
        piexif.GPSIFD.GPSLatitudeRef: lat_ref.encode(),
        piexif.GPSIFD.GPSLatitude: lat_dms,
        piexif.GPSIFD.GPSLongitudeRef: lon_ref.encode(),
        piexif.GPSIFD.GPSLongitude: lon_dms,
        piexif.GPSIFD.GPSAltitude: (0, 1),  # Set altitude to 0 for simplicity
        piexif.GPSIFD.GPSAltitudeRef: 0  # Above sea level
    }

    # Update EXIF data with the GPS IFD
    exif_dict['GPS'] = gps_ifd

    # Convert the EXIF dict back to bytes and insert it into the image
    exif_bytes = piexif.dump(exif_dict)
    piexif.insert(exif_bytes, image_path, output_path)
    
    print(f"GPS metadata added to {output_path}")

# Example usage with fake parking spot coordinates in Newton, MA

# Parking Spot 1 coordinates
parking_spot_1_latitude = 42.3371  # Latitude of a parking spot in Newton, MA
parking_spot_1_longitude = -71.2092  # Longitude of a parking spot in Newton, MA

# Image paths
image_path = r"C:\Users\12023\Downloads\extracted_images\images\GOPR0090.JPG"
output_path = r"C:\Users\12023\Downloads\extracted_images\images\GOPR0090_with_gps_1.JPG"

# Add GPS metadata for Parking Spot 1
add_gps_metadata(image_path, output_path, parking_spot_1_latitude, parking_spot_1_longitude)

# Function to print EXIF data using piexif
def print_piexif_tags(filepath):
    # Load EXIF data using piexif
    exif_dict = piexif.load(filepath)

    # Print all EXIF data
    for ifd_name in exif_dict:
        print(f"{ifd_name}:")
        if isinstance(exif_dict[ifd_name], dict):
            for tag in exif_dict[ifd_name]:
                print(f"  {piexif.TAGS[ifd_name][tag]['name']}: {exif_dict[ifd_name][tag]}")

# Example usage
print_piexif_tags(output_path)

# Function to print all EXIF tags using exifread
def print_all_exif_tags(filepath):
    with open(filepath, 'rb') as f:
        tags = exifread.process_file(f)
        for tag in tags.keys():
            print(f"{tag}: {tags[tag]}")

# Example usage with exifread
print_all_exif_tags(output_path)
