import slackclient as sc
import time
from weather import *  # PyCharm highlights this as wrong, but it's fine. The methods defined here also work.
from common import *
import xml.etree.ElementTree as et
import os
from chart import *
import datetime
from aurora import *


def get_config():
    tree = et.parse(os.getcwd() + '/../config.xml')
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
The currently supported locations are: ubc, porteau, macmillan, kobau, meritt, boundary, mitchell.
The terms you enter can be in any order. Do note: every term must be one word. Use "Porteau", not "Porteau Cove".

Let Mia know if there's anything I can do to be more useful! (as long as it won't take too long to code...)
"""
legal_text = """
This project uses OpenWeatherMap's API for weather reporting, and Slack's RealTimeMessaging API for Slack integration.
Both are used through Python through the pyowm and slackclient PyPI packages, respectively.
This project is licenced under the MIT licence, as are both those packages. Contact Mia Kramer for more information."""


def handle_command(command, channel):
    if command.special_req != SpecialCommand.none:
        if command.special_req == SpecialCommand.help:
            response = help_text
        elif command.special_req == SpecialCommand.aurora:
            client.api_call("chat.postMessage", channel=channel, text="Retrieving 3 day aurora forecast...", as_user=True)
            response = check_aurora_forecast()
        elif command.special_req == SpecialCommand.legal:
            response = legal_text
        elif command.special_req == SpecialCommand.ping:
            response = "Pong"
        elif command.special_req == SpecialCommand.chart:
            if command.location is not None:
                client.api_call("chat.postMessage", channel=channel, text="I'm looking up the chart for: " + \
                                                                          command.location.capitalize() + ".", as_user=True)
                charturl = fetch_image_url(command.location)
                if charturl is not None:
                    client.api_call("chat.postMessage", channel=channel, attachments='[{"image_url":"' +
                                                                                     charturl + '", "title":"chart"}]',
                                    text="", as_user=True)
                    response = None
                else:
                    response = "I'm sorry, I couldn't get that chart."
            else:
                response = "I need a place I recognize to give you a chart."
        else:
            response = "I'm sorry, I didn't understand that. Try again or type: `@weatherbot help`."
    else:
        client.api_call("chat.postMessage", channel=channel, text="I'm looking up the weather for: " + \
                                                                  command.target_date.capitalize() + ", at: " + \
                                                                  command.location.capitalize() + ".", as_user=True)
        response = get_weather(command)
    if response is not None:
        client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)


def parse_slack_output(slack_rtm_output):
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None



def main():
    while not client.rtm_connect():
        print("Weatherbot is not running. Will try again in 30 seconds.")
        print("Double check the bot token.")
        time.sleep(30)
    debug and print("Weatherbot is running.")
    client.api_call('chat.postMessage', channel='#testing_weatherbot', text='Weatherbot start successful.', as_user=True)
    target_time = datetime.datetime.today()

    while True:
        command, channel = parse_slack_output(client.rtm_read())
        if command and channel:
            debug and print("Received command...")
            command = Command(command)
            handle_command(command, channel)
        if time.localtime().tm_min == target_time.minute:
            resp = check_aurora()
            if resp is not None:
                response = "AURORA ALERT: According to the NOAA Aurora Forecast, there is an increased possibility of"
                response += " seeing the Northern Lights in the next half hour.\nThe probability is: {}% in the {} area.".format(resp.prob, resp.area)
                client.api_call('chat.postMessage', channel='#announcements', text=response, as_user=True)
            target_time = datetime.datetime.today() + datetime.timedelta(minutes=30)
        time.sleep(READ_WEBSOCKET_DELAY)


if __name__ == "__main__":
    main()
