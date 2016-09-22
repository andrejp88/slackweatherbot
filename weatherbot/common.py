from enum import Enum
import datetime


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

locations      = ["ubc", "porteau", "macmillan"]
location_ref   = {"ubc" : "49.2653645,-123.2520194", "porteau" : "49.5571242,-123.2384998",
                  "macmillan" : "49.2763368,-123.1450727"}
location_short = {"ubc" : "ubc", "porteau" : "porteau", "macmillan" : "macmillan", "van" : "ubc", "vancouver" : "ubc"}


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
        delta = target - today
        if delta.days < 0:
            delta = datetime.datetime(today.year+1, month, date)
        if delta.days > 14:
            return Date_Request.too_far
        elif delta.days > 5:
            return Date_Request.daily
        else:
            return Date_Request.forecast

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


class SpecialCommand(Enum):
    none = 0  # none
    help = 1  # help menu requested
    not_rec = 2  # request not recognized
    legal = 3  # legal stuff
    ping = 4  # for checking if the bot is running


class Command:
    location = None
    target_date = None
    special_req = SpecialCommand.none
    date_request = None

    def __init__(self, request):
        items = request.split(' ')
        if "help" in items:
            self.special_req = SpecialCommand.help
        elif "legal" in items:
            self.special_req = SpecialCommand.legal
        elif "ping" in items:
            self.special_req = SpecialCommand.ping

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
                self.special_req = SpecialCommand.not_rec

        elif len(items) == 2:
            found_date = False
            found_loc = False
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
                    self.special_req = SpecialCommand.not_rec

            if found_loc and not found_date:
                self.special_req = SpecialCommand.not_rec

        elif len(items) == 3:
            locloc = -1
            for i in location_short:
                for j in range(len(items)):
                    if i == items[j]:
                        locloc = j
                        self.location = location_short[items[j]]
                        break
            if locloc == -1:
                self.special_req = SpecialCommand.not_rec
            else:
                tempitems = []
                for i in range(len(items)):
                    if i != locloc:
                        tempitems.append(items[i])
                response = monthdayparse(tempitems)
                if response is not None:
                    self.target_date = response
                    self.location = "ubc"
                else:
                    self.special_req = SpecialCommand.not_rec

        else:
            self.special_req = SpecialCommand.not_rec

        if self.special_req == SpecialCommand.none:
            self.date_request = _check_date(self.target_date)

    def render(self):
        string = "Command:\n"
        string += "Special command: " + str(Command.special_req).split(".")[1]
        string += "Location: " + str(Command.location) + "\n"
        string += "Time: " + str(Command.target_date)
        return string
