from enum import Enum

class SpecialCommand(Enum):
    none = 0  # none
    help = 1  # help menu requested
    not_rec = 2  # request not recognized
    legal = 3  # legal stuff


class Command:
    location = None
    target_date = None
    special_req = SpecialCommand.none

    def __init__(self, request):
        items = request.split(' ')
        if "help" in items:
            self.special_req = SpecialCommand.help
        elif "legal" in items:
            self.special_req = SpecialCommand.legal

        elif len(items) == 0:
            self.location = "ubc"
            self.target_date = "current"

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
                        self.target_date = "current"
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

    def render(self):
        string = "Command:\n"
        string += "Special command: " + str(Command.special_req).split(".")[1]
        string += "Location: " + str(Command.location) + "\n"
        string += "Time: " + str(Command.target_date)
        return string


class Date_Request(Enum):
    observation = 0
