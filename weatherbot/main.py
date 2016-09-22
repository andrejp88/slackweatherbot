import slackclient as sc
import time
from weather import *  # PyCharm highlights this as wrong, but it's fine. The methods defined here also work.
from common import *
import xml.etree.ElementTree as et
import os.path
import datetime


def get_config():
    tree = et.parse(os.path.dirname(__file__) + '/../config.xml')
    root = tree.getroot()

    OWM_TOKEN   = None
    SLACK_TOKEN = None
    BOT_ID      = None
    debug       = None

    for child in root:
        if child.tag == "owm-token":
            OWM_TOKEN = child.text
        elif child.tag == "slack-token":
            SLACK_TOKEN = child.text
        elif child.tag == "slack-id":
            BOT_ID = child.text
        elif child.tag == "debug":
            debug = child.text

    if OWM_TOKEN is None or SLACK_TOKEN is None or BOT_ID is None:
        print("Could not read config. Exiting...")
        exit(2)
    return OWM_TOKEN, SLACK_TOKEN, BOT_ID, debug


OWM_TOKEN, SLACK_TOKEN, BOT_ID, debug = get_config()
AT_BOT    = "<@" + BOT_ID + ">"
client = sc.SlackClient(SLACK_TOKEN)



READ_WEBSOCKET_DELAY = 1

months_short   = {"jan" : "january", "feb" : "february", "mar" : "march", "apr" : "april",
                  "may" : "may", "jun" : "june", "jul" : "july", "aug" : "august",
                  "sep" : "september", "oct" : "october", "nov" : "november", "dec" : "december"}
special_dates  = ["now", "tomorrow", "tonight", "today"]
months_ord     = {"jan" : 1, "feb" : 2, "mar" : 3, "apr" : 4,
                  "may" : 5, "jun" : 6, "jul" : 7, "aug" : 8,
                  "sep" : 9, "oct" : 10, "nov" : 11, "dec" : 12}
dates          = [str(i) for i in range(1, 32)]
days_per_month = {"jan" : 31, "feb" : 29, "mar" : 31, "apr" : 30,
                  "may" : 31, "jun" : 30, "jul" : 31, "aug" : 31,
                  "sep" : 30, "oct" : 31, "nov" : 30, "dec" : 31}

locations      = ["ubc", "porteau", "macmillan"]
location_ref   = {"ubc" : "49.2653645,-123.2520194", "porteau" : "49.5571242,-123.2384998",
                  "macmillan" : "49.2763368,-123.1450727"}
location_short = {"ubc" : "ubc", "porteau" : "porteau", "macmillan" : "macmillan", "van" : "ubc", "vancouver" : "ubc"}

help_text = """
Hello! I'm weatherbot.

You can ask for my help by calling my name (with @), and then entering between one and three items.
If you enter just a location, I will return the current weather there.
If you enter just a date, I will return the forecast for that date at UBC.
If you enter a date and a location, I will return the forecast for that date at that location.
Here are a couple of examples:
`september 27` - the forecast for September 27 at UBC.
`oct 5 porteau` - the forecast for October 5 at Porteau Cove.
`porteau tomorrow` - tomorrow's forecast at Poretau Cove.
`tonight macmillan` - tonight's forecast at the MacMillan Observatory.
`now` - the current weather at UBC.
`porteau` - the current weather at Porteau Cove.

You can either use one of the special dates (`now`, `tonight`, `tomorrow`, and `today`) or a month and a date.
The currently supported locations are: ubc, porteau, macmillan.
The terms you enter can be in any order. Do note: every term must be one word. Use "Porteau", not "Porteau Cove".

Let Mia know if there's anything I can do to be more useful! (as long as it won't take too long to code...)
"""
legal_text = """
This project uses OpenWeatherMap's API for weather reporting, and Slack's RealTimeMessaging API for Slack integration.
Both are used through Python through the pyowm and slackclient PyPI packages, respectively.
This project is licenced under the MIT licence, as are both those packages. Contact Mia Kramer for more information."""


def check_dates(date):
    if date in special_dates:
        return date


def monthdayparse(items):
    if items[0] in dates:
        for i in months_short:
            if i in items[1]:
                if eval(items[0]) <= days_per_month[items[1][0:3]]:
                    target_date = months_short[items[1][0:3]] + " " + items[0]
                    break
                else:
                    return None
    elif items[1] in dates:
        for i in months_short:
            if i in items[0]:
                if eval(items[1]) <= days_per_month[items[0][0:3]]:
                    target_date = months_short[items[0][0:3]] + " " + items[1]
                    break
                else:
                    return None
    else:
        return None
    try:
        return target_date
    except:
        return None


def handle_command(command, channel):
        if command.special_req != SpecialCommand.none:
            if command.special_req == SpecialCommand.help:
                response = help_text
            elif command.special_req == SpecialCommand.legal:
                response = legal_text
            else:
                response = "I'm sorry, I didn't understand that. Try again or type: `@weatherbot help`."
        else:
            client.api_call("chat.postMessage", channel=channel, text="I'm looking up the weather for: " + \
                                                                      command.target_date.capitalize() + ", at: " +\
                                                                      command.location.capitalize() + ".", as_user=True)
            weather = get_weather(command.target_date, get_coords(command.location))
            if weather is not None:
                response = format_weather(weather, command.target_date)
            else:
                response = "I'm sorry, I couldn't get the weather."
        client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)


def parse_slack_output(slack_rtm_output):
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None


def get_coords(loc):
    return eval(location_ref[loc])


if __name__ == "__main__":
    while not client.rtm_connect():
        print("Weather bot is not running. Will try again in 30 seconds.")
        print("Double check the bot token?")
        time.sleep(30)
    debug and print("Weather bot is running.")
    client.api_call('chat.postMessage', channel='#testing_weatherbot', text='@miak Bot started.', as_user=True)
    while True:
        command, channel = parse_slack_output(client.rtm_read())
        if command and channel:
            debug and print("Received command...")
            command = Command(command)
            debug and print("Command:")
            debug and print(Command.render())
            handle_command(command, channel)
        time.sleep(READ_WEBSOCKET_DELAY)
