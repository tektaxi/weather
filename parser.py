from geopy import Nominatim
import requests
import json


def get_weather(user_location):
    geolocator = Nominatim(user_agent="weather_app")
    location = geolocator.geocode(user_location)
    lat = location.latitude
    lon = location.longitude

    apikey = "83a22c5c5ac2596bb043c7f8a6d8e7ef"

    response = requests.get(f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&appid={apikey}")
    res_text = response.text
    data = json.loads(res_text)
    current = data["current"]
    c_weather = current["weather"]
    w_fix = c_weather[0]

    master_json = {
        "location": [],
        "current": [],
        "hourly": [],
        "daily": []
    }

    location_request = requests.get(f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=jsonv2&zoom=10&namedetails=1&accept-language=en-US")
    loc_text = location_request.text
    location_data = json.loads(loc_text)

    location_name = location_data["display_name"]

    address = location_data["address"]
    loc = dict()

    loc["display_name"] = location_name
    loc["address"] = address
    master_json["location"] = loc

    c = dict()
    c["time"] = current["dt"]
    c["temp"] = current["temp"]
    c["description"] = w_fix["description"]
    c["id"] = w_fix["id"]
    c["icon"] = w_fix["icon"]

    master_json["current"] = c

    hourly = data["hourly"]

    hours = []

    for i in range(24):
        tab = {}
        hour = hourly[i]
        weather_ini = hour["weather"]
        weather = weather_ini[0]

        tab["time"] = hour["dt"]
        tab["temp"] = hour["temp"]
        tab["description"] = weather["description"]
        tab["id"] = weather["id"]
        tab["icon"] = weather["icon"]
        tab["pop"] = hour["pop"]
        hours.append(tab)

    master_json["hourly"] = hours

    daily = data["daily"]
    days = []

    for i in range(7):
        tab = {}
        day = daily[i]
        weather_ini = day["weather"]
        weather = weather_ini[0]

        temp = day["temp"]

        tab["time"] = day["dt"]
        tab["day"] = temp["day"]
        tab["min"] = temp["min"]
        tab["max"] = temp["max"]
        tab["description"] = weather["description"]
        tab["id"] = weather["id"]
        tab["icon"] = weather["icon"]
        tab["pop"] = day["pop"]

        days.append(tab)

    master_json["daily"] = days
    return_json = {"api-return": master_json}

    return return_json

