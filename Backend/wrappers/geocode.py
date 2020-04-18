from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

# Convert address to an object containing latitude, longitude
def get_lat_lon_by_address(address):
    geolocator = Nominatim(user_agent="Twitter Trends", scheme='http')
    try:
        location = geolocator.geocode(address, timeout=5)
        lat, lon = location.latitude, location.longitude
        return lat, lon
    except GeocoderTimedOut as e:
        print("Error: geocode failed on input %s with message %s" % (e.msg))


if __name__ == '__main__':
    city = 'Philadelphia'
    lat, lon = get_lat_lon_by_address(city)
    print(lat, lon)