from common import *
import datetime

fail_message = "I'm sorry, I couldn't get the weather."

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
        return forecast.get_forecast()
    except:
        return None


def get_daily(coords):
    try:
        forecast = owm_client.daily_forecast_at_coords(coords[0], coords[1])
        return forecast.get_forecast()
    except:
        return None


def get_weather(command):
    coords = eval(location_ref[command.location])
    if command.date_request == Date_Request.observation:
        weather = get_obs(coords)
        if weather is not None:
            return format_weather_obs(weather)
        else:
            return fail_message
    elif command.date_request == Date_Request.too_far:
        return "I'm sorry, but that date is too far away."
    elif command.date_request == Date_Request.hourly:
        weather = get_3hr(coords)
        if weather is not None:
            return format_weather_3hr(weather.get_weathers(), command.target_date)
        else:
            return fail_message
    else:
        weather = get_daily(coords)
        if weather is not None:
            return format_weather_daily(weather, command.target_date)
        else:
            return fail_message


def format_time(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime('%b %d at %H:%M:%S')


def format_time_short(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime('%H:%M')


def format_weather_obs(weather):
    string  = "Currently: \n"
    string += str(weather.get_temperature('celsius')['temp']) + "ºC.\n"
    string += "The cloud coverage is: " + str(weather.get_clouds()) + "%.\n"
    string += "The humidity is: " + str(weather.get_humidity()) + "%\n"
    string += "The wind speed is: " + str(weather.get_wind()['speed']) + " kph\n"
    return string


def format_weather_3hr(weather, target_date):
    string = ""
    if target_date == "tonight":
        current_date = datetime.datetime.today()
        end_date     = current_date + datetime.timedelta(hours=24-current_date.hour) + datetime.timedelta(hours=3, minutes=59)

        string  = "Tonight: \n"
        using_weathers = [i for i in weather if current_date <= datetime.datetime.fromtimestamp(i.get_reference_time()) <= end_date]

        for w in using_weathers:
            string += "At " + format_time_short(w.get_reference_time()) + ":\n"
            string += str(w.get_temperature('celsius')['temp']) + "ºC; "
            string += str(w.get_clouds()) + "% clouds; "
            string += str(w.get_humidity()) + "% humidity; "
            string += str(w.get_wind()['speed']) + " kph wind.\n\n"

    elif target_date == "tomorrow":
        current_date = datetime.datetime.today()
        start_date   = current_date + datetime.timedelta(hours=23-current_date.hour, minutes=60-current_date.hour)
        end_date     = start_date   + datetime.timedelta(hours=27)

        string  = "Tomorrow: \n"
        using_weathers = [i for i in weather if
                          start_date <= datetime.datetime.fromtimestamp(i.get_reference_time()) <= end_date]

        for w in using_weathers:
            string += "At " + format_time_short(w.get_reference_time()) + ":\n"
            string += str(w.get_temperature('celsius')['temp']) + "ºC; "
            string += str(w.get_clouds()) + "% clouds; "
            string += str(w.get_humidity()) + "% humidity; "
            string += str(w.get_wind()['speed']) + " kph wind.\n\n"

    else:
        current_date = datetime.datetime.today()
        dates        = target_date.split(" ")
        start_date   = datetime.datetime(year=current_date.year, month=int(months_ord[dates[0][0:3]]),
                                         day=int(dates[1]))
        if current_date.month == 12 and start_date.month == 1:
            start_date = datetime.datetime(year=current_date.year, month=int(months_ord[dates[0][0:3]]),
                                           day=int(dates[1]))

        end_date     = start_date + datetime.timedelta(days=1)

        string = "On "+target_date.capitalize()+":\n"
        using_weathers = [i for i in weather if
                          start_date <= datetime.datetime.fromtimestamp(i.get_reference_time()) <= end_date]

        for w in using_weathers:
            string += "At " + format_time_short(w.get_reference_time()) + ":\n"
            string += str(w.get_temperature('celsius')['temp']) + "ºC; "
            string += str(w.get_clouds()) + "% clouds; "
            string += str(w.get_humidity()) + "% humidity; "
            string += str(w.get_wind()['speed']) + " kph wind.\n\n"


    return string


def format_weather_daily(weather, target_date):
    string  = "Long-term forecasts have not yet been implemented. For astronomy they're probably useless, but Mia will get around to it soonish."
    return string