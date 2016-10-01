from enum import Enum
import datetime
import pyowm
import xml.etree.ElementTree as et
import os.path
from weatherbot.locations import *
import re


### CONSTANTS
READ_WEBSOCKET_DELAY = 1

months_short   = {"jan" : "january", "feb" : "february", "mar" : "march", "apr" : "april",
                  "may" : "may", "jun" : "june", "jul" : "july", "aug" : "august",
                  "sep" : "september", "oct" : "october", "nov" : "november", "dec" : "december"}
special_dates  = ["now", "tomorrow", "tonight", "today"]
dates          = [str(i) for i in range(1, 32)]
days_per_month = {"jan" : 31, "feb" : 29, "mar" : 31, "apr" : 30,
                  "may" : 31, "jun" : 30, "jul" : 31, "aug" : 31,
                  "sep" : 30, "oct" : 31, "nov" : 30, "dec" : 31}
months_ord     = {"jan" : 1, "feb" : 2, "mar" : 3, "apr" : 4,
                  "may" : 5, "jun" : 6, "jul" : 7, "aug" : 8,
                  "sep" : 9, "oct" : 10, "nov" : 11, "dec" : 12}

# The minimum number of letters required to be sure of what month is being discussed,
# and the regex pattern corresponding to the valid days in that month.
pattern31days = "0*([1-9]|(1|2)[0-9]|3(0|1))"
pattern30days = "0*([1-9]|(1|2)[0-9]|30)"
months_disambig_with_days = {"ja" : pattern31days,
                             "f"  : "0*([1-9]|1[0-9]|2[0-8])",
                             "mar": pattern31days,
                             "ap" : pattern30days,
                             "may": pattern31days,
                             "jun": pattern30days,
                             "jul": pattern31days,
                             "au" : pattern31days,
                             "s"  : pattern30days,
                             "o"  : pattern31days,
                             "n"  : pattern30days,
                             "d"  : pattern31days}


### OWM
def get_token():
    tree = et.parse(os.path.dirname(__file__) + '/../config.xml')
    root = tree.getroot()
    for child in root:
        if child.tag == "owm-token":
            return child.text


OWM_TOKEN = get_token()
owm_client = pyowm.OWM(str(OWM_TOKEN))

class Date_Request(Enum):
    observation = 0
    hourly      = 1
    daily       = 2
    too_far     = 3


def _check_date(date):
    if date == "now":
        return Date_Request.observation
    elif date in ("today", "tonight", "tomorrow"):
        return Date_Request.hourly
    else:
        today  = datetime.datetime.today()
        parsed = date.split(" ")
        month  = int(months_ord[parsed[0][0:3]])
        date   = int(parsed[1])
        target = datetime.datetime(today.year, month, date)
        delta  = target - today
        if delta.days < -1:
            target = datetime.datetime(today.year+1, month, date)
            delta  = target - today
        if delta.days > 14:
            return Date_Request.too_far
        elif delta.days > 5:
            return Date_Request.daily
        else:
            return Date_Request.hourly

    # except:
    #     print("Check date failed.")
    #     return None


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


class CommandType(Enum):
    """
    The type of command requested.
    """
    regular    = 0  # regular command - only a date and/or a location was provided
    help       = 1  # help menu requested
    invalid    = 2  # request not recognized
    legal      = 3  # legal stuff
    ping       = 4  # for checking if the bot is running
    chart      = 5  # cleardarksky chart
    aurora     = 6  # aurora forecast


def generate_date_pattern():
    date_pattern = "("

    # Add the special relative dates
    for i in special_dates:
        date_pattern += i + "|"

    date_pattern = date_pattern.strip('|')
    date_pattern += ")|("

    # "Au", "aug", "August", "AUGUSTUSCAESAR", "aUrIgA" all match August.
    # Might not be bad for ~internationalijeriodf~ i18n, not that anyone's ever going to use it in any other language.
    for month, month_length_pattern in months_disambig_with_days.items():
        date_pattern += month + "[a-z]* " + month_length_pattern + "|"

    date_pattern = date_pattern.strip('|')
    date_pattern += ")"

    print(date_pattern)

    return re.compile(date_pattern)


class Command:
    location = None             # the location the user is requesting weather for
    target_date = None          # the date the user is requesting weather for
    type = CommandType.regular  # the type of command - certain commands need to be processed differently
    date_request = None         # no idea

    date_regex = generate_date_pattern()

    def __init__(self, request):
        """
        Constructs a `Command` object

        :param request: string
        """

        # Andrej's code:
        request = request.lower()
        if request == "help":
            self.type = CommandType.help
        elif request == "legal":
            self.type = CommandType.legal
        elif request == "ping":
            self.type = CommandType.ping
        elif request == "aurora":
            self.type = CommandType.aurora
        elif len(request) == 0:
            # If no arguments are given, just return the current weather at UBC
            self.type = CommandType.regular
            self.location = "ubc"
            self.target_date = "now"
        else:
            # todo: check whether the command fits the regex for "chart date location" in any order

            if True:
                self.type = CommandType.regular
            else:
                self.type = CommandType.invalid

        # Mia's code:
        items = request.split(' ')
        if "help" in items:
            self.type = CommandType.help
        elif "legal" in items:
            self.type = CommandType.legal
        elif "ping" in items:
            self.type = CommandType.ping

        elif len(items) == 0:
            self.location = "ubc"
            self.target_date = "now"

        elif len(items) == 1:
            found = False
            for i in special_dates:
                if i in items:
                    self.target_date = i
                    self.location = "ubc"
                    found = True
                    break
            if not found:
                for i in location_short:
                    if i in items:
                        self.location = location_short[i]
                        self.target_date = "now"
                        found = True
                        break
            if not found:
                if "aurora" in items:
                    self.type = CommandType.aurora
                    found = True
            if not found:
                self.type = CommandType.invalid

        elif len(items) == 2:
            found_date = False
            found_loc = False
            if "chart" in items:
                self.type = CommandType.chart
                found_date = True

            if not(found_date):
                for i in special_dates:
                    if i in items:
                        self.target_date = i
                        found_date = True
                        break

            for i in location_short:
                if i in items:
                    self.location = location_short[i]
                    found_loc = True
                    break

            if not found_date and not found_loc:
                response = monthdayparse(items)
                if response is not None:
                    self.location = "ubc"
                    self.target_date = response
                else:
                    self.type = CommandType.invalid

            if found_loc and not found_date:
                self.type = CommandType.invalid

        elif len(items) == 3:
            locloc = -1
            for i in location_short:
                for j in range(len(items)):
                    if i == items[j]:
                        locloc = j
                        self.location = location_short[items[j]]
                        break
            if locloc == -1:
                self.type = CommandType.invalid
            else:
                tempitems = []
                for i in range(len(items)):
                    if i != locloc:
                        tempitems.append(items[i])
                response = monthdayparse(tempitems)
                if response is not None:
                    self.target_date = response
                else:
                    self.type = CommandType.invalid

        else:
            self.type = CommandType.invalid

        if self.type == CommandType.regular:
            self.date_request = _check_date(self.target_date)

    def render(self):
        string = "Command:\n"
        string += "Special command: " + str(Command.type).split(".")[1]
        string += "Location: " + str(Command.location) + "\n"
        string += "Time: " + str(Command.target_date)
        return string


class AuroraReport:
    area = None
    prob = None
    def __init__(self, area, prob):
        self.area = area
        self.prob = prob
