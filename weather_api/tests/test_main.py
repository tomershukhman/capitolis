import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app
from weather_service import is_good_day_for_outdoor

client = TestClient(app)

@patch('weather_service.fetch_weather')
def test_get_weather_good_day(mock_fetch_weather):
    mock_fetch_weather.return_value = {
        "temperature": 20,
        "description": "clear sky"
    }

    response = client.get("/weather/London")

    assert response.status_code == 200
    assert response.json() == {
        "city": "London",
        "temperature": 20,
        "description": "clear sky",
        "good_for_outdoor": True
    }

@patch('weather_service.fetch_weather')
def test_get_weather_bad_day(mock_fetch_weather):
    mock_fetch_weather.return_value = {
        "temperature": 10,
        "description": "rain"
    }

    response = client.get("/weather/London")

    assert response.status_code == 200
    assert response.json() == {
        "city": "London",
        "temperature": 10,
        "description": "rain",
        "good_for_outdoor": False
    }

@patch('weather_service.fetch_weather')
def test_get_weather_invalid_city(mock_fetch_weather):
    mock_fetch_weather.side_effect = Exception("City not found")

    response = client.get("/weather/InvalidCity")

    assert response.status_code == 400
    assert response.json() == {"detail": "City not found"}

def test_is_good_day_for_outdoor():
    assert is_good_day_for_outdoor(20, "clear sky") == True
    assert is_good_day_for_outdoor(10, "rain") == False
    assert is_good_day_for_outdoor(30, "clear sky") == False
    assert is_good_day_for_outdoor(18, "few clouds") == True
    assert is_good_day_for_outdoor(22, "light rain") == False
