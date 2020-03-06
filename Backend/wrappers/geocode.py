from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="Twitter Trends")

# Convert address to an object containing latitude, longitude
def geocoding(address):
    location = geolocator.geocode(address)
    lat, long = int(location.latitude), int(location.longitude)
    return lat, long


if __name__ == '__main__':
    city = 'Philadelphia'
    location = geocoding(city)
    # print(location.raw['place_id'])