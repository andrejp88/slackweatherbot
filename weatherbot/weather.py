import pyowm
import xml.etree.ElementTree as et
import os.path
import datetime
from common import *


def get_token():
    global OWM_TOKEN
    tree = et.parse(os.path.dirname(__file__) + '/../config.xml')
    root = tree.getroot()
    for child in root:
        if child.tag == "owm-token":
            OWM_TOKEN = child.text


get_token()
owm_client = pyowm.OWM(str(OWM_TOKEN))
# cache      = pyowm.caches.lrucache.LRUCache()


def get_obs(date, coords):
    try:
        observation = owm_client.weather_at_coords(coords[0], coords[1])
        weather = observation.get_weather()
        return weather
    except:
        return None


def get_3hr(date, coords):
    try:
        forecast = owm_client.three_hours_forecast_at_coords(coords[0], coords[1])
    except:
        return None


def get_weather(date, coords):
    if date == "now":
        return get_obs(date, coords)
    elif date in ("today", "tonight"):
        try:
            pass
        except:
            return None
    elif date == "tomorrow":
        try:
            pass
        except:
            return None
    else:
        try:
            pass
        except:
            return None


def format_time(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime('%b %d at %H:%M:%S')


def format_time_short(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime('%H:%M')


def format_weather(weather, date):
    pass


def format_weather_now(weather):
    string  = "Currently: \n"
    string += str(weather.get_temperature('celsius')['temp']) + "ºC.\n"
    string += "The cloud coverage is: " + str(weather.get_clouds()) + "%.\n"
    string += "The humidity is: " + str(weather.get_humidity()) + "%\n"
    string += "The wind speed is: " + str(weather.get_wind()['speed']) + " kph\n"
    string += "Weather last updated: " + format_time(weather.get_reference_time()) + "."
    return string


def format_weather_today(weather):
    string  = format_weather_now(weather)
    string += "\n\n"
    string += format_weather_tonight(weather)
    string += "\n\nSunrise: " + format_time_short(weather.get_sunrise_time())
    string += "\nSunset: " + format_time_short(weather.get_sunset_time())


def format_weather_tonight(weather):
    string  = "Tonight:"
    string += ""
