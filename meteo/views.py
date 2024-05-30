from datetime import datetime

import geocoder
import requests  # Correctly import the requests module
from django.shortcuts import render


def temp_here():
    endpoint = "https://api.open-meteo.com/v1/forecast"
    location = geocoder.ip('me').latlng
    if not location:
        return {"error": "Could not determine location"}

    api_request = f"{endpoint}?latitude={location[0]}&longitude={location[1]}&hourly=temperature_2m"
    now = datetime.now()
    hour = now.hour

    try:
        response = requests.get(api_request)
        response.raise_for_status()  # This will raise an HTTPError if the HTTP request returned an unsuccessful status code
        data = response.json()

        # Assuming the API returns hourly data in a list for the current day
        temperature_data = data.get('hourly', {}).get('temperature_2m', [])

        if not temperature_data:
            return {"error": "No temperature data available"}

        current_hour_temperature = temperature_data[hour]
        return {"current_temperature": current_hour_temperature}
    except requests.RequestException as e:
        return {"error": str(e)}
    except (IndexError, KeyError) as e:
        return {"error": f"Unexpected data format: {str(e)}"}

# Now you can run temp_here() to get the temperature data
