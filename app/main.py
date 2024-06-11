from fastapi import FastAPI, HTTPException
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Configuration
GEOCODE_API_KEY = os.getenv("GEOCODE_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

app = FastAPI()


def get_lat_lon(city, geocode_api_key):
    """
    Get the latitude and longitude of a city using the Google Geocoding API.

    Parameters:
    - city (str): The city name to geocode.
    - geocode_api_key (str): Your Google Geocoding API key.

    Returns:
    - (lat, lon): Tuple containing latitude and longitude.
    """
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={city}&key={geocode_api_key}"
    response = requests.get(url)
    data = response.json()

    if data['status'] == 'OK':
        lat = data['results'][0]['geometry']['location']['lat']
        lon = data['results'][0]['geometry']['location']['lng']
        return lat, lon
    else:
        raise HTTPException(status_code=400, detail=f"Error geocoding city: {data['status']}")


def get_current_weather(lat, lon, weather_api_key):
    """
    Get current weather data for a given latitude and longitude using the OpenWeatherMap API.

    Parameters:
    - lat (float): Latitude.
    - lon (float): Longitude.
    - weather_api_key (str): Your OpenWeatherMap API key.

    Returns:
    - data (dict): The weather data.
    """
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={weather_api_key}"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        return data
    else:
        raise HTTPException(status_code=response.status_code,
                            detail=f"Error fetching weather data: {response.status_code}")


@app.get("/weatherapi/current_weather/{city}")
def fetch_current_weather(city: str):
    """
    Endpoint to fetch current weather data for a city.

    Parameters:
    - city (str): The name of the city to get weather for.

    Returns:
    - weather_data (dict): The weather data.
    """
    try:
        # Step 1: Get latitude and longitude
        lat, lon = get_lat_lon(city, GEOCODE_API_KEY)

        # Step 2: Get current weather data
        weather_data = get_current_weather(lat, lon, WEATHER_API_KEY)

        return weather_data
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run the app with `uvicorn main:app --reload`
