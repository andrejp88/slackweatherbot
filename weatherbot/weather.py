import pyowm
import xml.etree.ElementTree as et
import os.path
import datetime
from common import *

fail_message = "I'm sorry, I couldn't get the weather."


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


def get_obs(coords):
    try:
        observation = owm_client.weather_at_coords(coords[0], coords[1])
        weather = observation.get_weather()
        return weather
    except:
        return None


def get_3hr(coords):
    try:
        forecast = owm_client.three_hours_forecast_at_coords(coords[0], coords[1])
    except:
        return None


def get_daily(coords):
    pass


def get_weather(command):
    if command.date_request == Date_Request.observation:
        weather = get_obs(location_ref[command.location])
        return format_weather_obs(weather)
    elif command.date_request == Date_Request.too_far:
        return "I'm sorry, but that date is too far away."
    elif command.date_request == Date_Request.hourly:
        weather = get_3hr(coords)
        return ""
    else:
        weather = get_daily(coords)
        return ""


def format_time(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime('%b %d at %H:%M:%S')


def format_time_short(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime('%H:%M')


def format_weather(weather, date):
    pass


def format_weather_obs(weather):
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
