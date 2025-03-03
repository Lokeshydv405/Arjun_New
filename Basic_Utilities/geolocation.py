# Importing necessary module
import requests

# Function to get location details
def get_location_details():
    try:
        # Fetch location data from ipinfo.io
        response = requests.get('https://ipinfo.io/json')
        data = response.json()
        
        # Extracting city, state, country, and location coordinates
        city = data.get('city', 'Unknown')
        state = data.get('region', 'Unknown')
        country = data.get('country', 'Unknown')
        loc = data.get('loc', 'Unknown')  # loc contains "latitude,longitude"
        
        # Splitting loc into latitude and longitude
        latitude, longitude = loc.split(',') if loc != 'Unknown' else ('Unknown', 'Unknown')
        
        return city, state, country, latitude, longitude
    except Exception as e:
        print(f"Error fetching location: {e}")
        return None, None, None, None, None

# Main method
if __name__ == "__main__":
    print("--------------- Location Details ---------------\n")
    
    # Fetch and display location details
    city, state, country, latitude, longitude = get_location_details()
    if city and state and country and latitude and longitude:
        print(f"You are in {city}, {state}, {country}")
        print(f"Latitude: {latitude}, Longitude: {longitude}")
    else:
        print("Failed to fetch location details.")
