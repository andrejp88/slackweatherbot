import numpy
import urllib.request
import shutil
from common import *

x_res = 0.32846715
y_res = 0.3515625

min_prob = 50

def lat_to_index(lat):
    return int((lat + 90) / y_res)

def long_to_index(long):
    return int((long + 180) / x_res)

def get_report():
    with urllib.request.urlopen("http://services.swpc.noaa.gov/text/aurora-nowcast-map.txt") as response, open("aurora.txt", 'wb') as outfile:
        shutil.copyfileobj(response, outfile)

def get_forecast():
    with urllib.request.urlopen("http://services.swpc.noaa.gov/text/3-day-forecast.txt") as response, open("aurora_fore.txt", 'wb') as outfile:
        shutil.copyfileobj(response, outfile)

def check_aurora():
    get_report()
    probs = numpy.loadtxt('aurora.txt', comments="#", dtype=numpy.int16)

    # check Vancouver area

    for x in range(long_to_index(-123.345284), long_to_index(-122.947415) + 1):
        for y in range(lat_to_index(49.131184), lat_to_index(49.368645) + 1):
            if probs[x, y] > min_prob:
                return AuroraReport("Vancouver", probs[x, y])

    # check Porteau Cove area
    for x in range(long_to_index(-123.241192), long_to_index(-123.221937) + 1):
        for y in range(lat_to_index(49.550582), lat_to_index(49.565458) + 1):
            if probs[x, y] > min_prob:
                return AuroraReport("Porteau", probs[x, y])

    # check Merritt area
    return None

def check_aurora_forecast():
    get_forecast()
    fore = open('aurora_fore.txt', 'r').readlines()
    resp = ""
    for i in range(6, 21):
        resp += fore[i] + "\n"
    return resp
