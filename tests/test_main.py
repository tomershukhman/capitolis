from fastapi import HTTPException
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
import sys
import os

# Add the parent directory of 'app' to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app, get_lat_lon, get_current_weather

client = TestClient(app)

@pytest.fixture
def mock_env(monkeypatch):
    monkeypatch.setenv("GEOCODE_API_KEY", "mock_geocode_api_key")
    monkeypatch.setenv("WEATHER_API_KEY", "mock_weather_api_key")

def mock_get_lat_lon(city, api_key):
    if city == "Mountain View":
        return 37.3861, -122.0839
    else:
        raise HTTPException(status_code=400, detail="Invalid city name")

def mock_get_current_weather(lat, lon, api_key):
    if lat == 37.3861 and lon == -122.0839:
        return {
            "coord": {"lon": -122.0839, "lat": 37.3861},
            "weather": [{"id": 800, "main": "Clear", "description": "clear sky", "icon": "01d"}],
            "base": "stations",
            "main": {
                "temp": 293.55,
                "feels_like": 293.13,
                "temp_min": 292.04,
                "temp_max": 295.37,
                "pressure": 1013,
                "humidity": 53
            },
            "visibility": 10000,
            "wind": {"speed": 1.5, "deg": 350},
            "clouds": {"all": 1},
            "dt": 1560350645,
            "sys": {
                "type": 1,
                "id": 5122,
                "message": 0.0139,
                "country": "US",
                "sunrise": 1560343627,
                "sunset": 1560396563
            },
            "timezone": -25200,
            "id": 5375480,
            "name": "Mountain View",
            "cod": 200
        }
    else:
        raise HTTPException(status_code=400, detail="Invalid coordinates")

def test_get_lat_lon(mock_env, mocker):
    mocker.patch('app.main.get_lat_lon', side_effect=mock_get_lat_lon)
    mocker.patch('app.main.get_current_weather', side_effect=mock_get_current_weather)
    response = client.get("/weatherapi/current_weather/Mountain%20View")
    assert response.status_code == 200
    data = response.json()
    assert "coord" in data
    assert "weather" in data
    assert data["name"] == "Mountain View"

def test_invalid_city(mock_env, mocker):
    mocker.patch('app.main.get_lat_lon', side_effect=mock_get_lat_lon)
    response = client.get("/weatherapi/current_weather/InvalidCityName")
    assert response.status_code == 400

def test_internal_server_error(mock_env, mocker):
    mocker.patch('app.main.get_lat_lon', side_effect=HTTPException(status_code=500, detail="Geocoding service failure"))
    response = client.get("/weatherapi/current_weather/Mountain%20View")
    assert response.status_code == 500
