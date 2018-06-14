#!/usr/bin/env python3

import argparse, string, json, requests, urllib
from datetime import datetime
from ruter.ruterapi import *

parser = argparse.ArgumentParser()
parser.add_argument("origin")
parser.add_argument("destination")
args = parser.parse_args()

transportMethods = {    0 : "🚶",
                        1 : "",
                        2 : "🚌",
                        3 : "",
                        4 : "",
                        5 : "",
                        6 : "🚆",
                        7 : "🚊",
                        8 : "🚇" }

def get_lat_lon():
    response = requests.get("https://freegeoip.net/json")
    jsonData = json.loads(response.content)
    return jsonData["latitude"], jsonData["longitude"]

def remove_punctuation(string):
    return string.translate({ord(c): None for c in "."})

def format_time(string):
    return datetime.strptime(string, "%Y-%m-%dT%H:%M:%S+02:00").strftime("%H:%M:%S")

for place in get_place_suggestions(args.origin):
    print(place)

#  latitude, longitude = get_lat_lon()

#  printString = "Latitude: {}\nLongitude: {}".format(latitude, longitude)
#  print(remove_punctuation(printString))


#  origin = args.origin # "Marmorveien 9 (Oslo)"

#  apiGetPlaceString = ("https://reisapi.ruter.no/Place/GetPlaces/?id="
        #  + urllib.parse.quote_plus(origin))

#  print("Using api string: " + apiGetPlaceString)

#  response = requests.get(apiGetPlaceString)

#  print("GET request status code: " + repr(response.status_code) + "\n")

#  jsonDataStopsOrigin = json.loads(response.content)

#  #print(jsonDataStops)
#  #print("Stops:")

#  originID = 0
#  destinationID = 0

#  for stop in jsonDataStopsOrigin:
    #  if stop["District"] == "Oslo" and stop["PlaceType"] == "Stop":
        #  originID = stop["ID"]
        #  break
#  #        print("\t" + "Name: " + stop["Name"])
#  #        print("\t" + "Plate type: " + stop["PlaceType"])

#  destination = args.destination # "Sandakerveien 24D (Oslo)"

#  apiGetPlaceString = "https://reisapi.ruter.no/Place/GetPlaces/?id=" + urllib.parse.quote_plus(destination)

#  response = requests.get(apiGetPlaceString)


#  print("GET request status code: " + repr(response.status_code) + "\n")

#  jsonDataStopsDestination = json.loads(response.content)

#  for stop in jsonDataStopsDestination:
    #  if stop["District"] == "Oslo" and stop["PlaceType"] == "Street":
        #  destinationID = stop["ID"]
        #  break
#  #        print("\t" + "Name: " + stop["Name"])
#  #        print("\t" + "Plate type: " + stop["PlaceType"])

#  apiRequest = "https://reisapi.ruter.no/Travel/GetTravels?fromPlace=" + repr(jsonDataStopsOrigin[0]["ID"]) + "&toPlace=" + repr(jsonDataStopsDestination[0]["ID"]) + "&isafter=true&proposals=5"

#  #apiRequest = "https://reisapi.ruter.no/Travel/GetTravels?fromPlace=" + repr(originID) + "&toPlace=" + repr(destinationID) + "&isafter=true&time=14062018070000&proposals=5"
#  response = requests.get(apiRequest)

#  print("Sending api request:" + apiRequest)

#  print("GET request status code: " + repr(response.status_code) + "\n")

#  if not response.content:
    #  print("Could not suggest any routes")
    #  exit()

#  jsonData = json.loads(response.content)

#  print("showing results from " + origin + " to " + destination)

#  for proposal in jsonData["TravelProposals"]:
    #  print("\n")
    #  print("Travel Time: " + proposal["TotalTravelTime"])
    #  print("Departure Time: " + format_time(proposal["DepartureTime"]))
    #  for stage in proposal["Stages"]:
        #  if stage["Transportation"] is not 0:
                                                                                    #  #2018-06-14T15:01:13+02:00
            #  print("{} {} -> {} -> {} {}".format(format_time(stage["DepartureTime"]), stage["DepartureStop"]["Name"], transportMethods[stage["Transportation"]],  format_time(stage["ArrivalTime"]), stage["ArrivalStop"]["Name"]))
        #  else:
            #  print("{} -> {} -> {}".format(format_time(stage["DepartureTime"]), transportMethods[stage["Transportation"]], format_time(stage["ArrivalTime"])))
    #  print("Arrival Time: " + format_time(proposal["ArrivalTime"]) + "\n")
    #  print("------------------------------------------------")