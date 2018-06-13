#!/usr/bin/env python3

import argparse, json, requests, urllib

parser = argparse.ArgumentParser()
parser.add_argument("origin")
parser.add_argument("destination")
args = parser.parse_args()

origin = args.origin # "Marmorveien 9 (Oslo)"

apiGetPlaceString = "https://reisapi.ruter.no/Place/GetPlaces/?id=" + urllib.parse.quote_plus(origin)

print("Using api string: " + apiGetPlaceString)

response = requests.get(apiGetPlaceString)

print("GET request status code: " + repr(response.status_code) + "\n")

jsonDataStopsOrigin = json.loads(response.content)

#print(jsonDataStops)
#print("Stops:")

originID = 0
destinationID = 0

for stop in jsonDataStopsOrigin:
    if stop["District"] == "Oslo" and stop["PlaceType"] == "Street":
        originID = stop["ID"]
        break
#        print("\t" + "Name: " + stop["Name"])
#        print("\t" + "Plate type: " + stop["PlaceType"])

destination = args.destination # "Sandakerveien 24D (Oslo)"

apiGetPlaceString = "https://reisapi.ruter.no/Place/GetPlaces/?id=" + urllib.parse.quote_plus(destination)

response = requests.get(apiGetPlaceString)


print("GET request status code: " + repr(response.status_code) + "\n")

jsonDataStopsDestination = json.loads(response.content)

for stop in jsonDataStopsDestination:
    if stop["District"] == "Oslo" and stop["PlaceType"] == "Street":
        destinationID = stop["ID"]
        break
#        print("\t" + "Name: " + stop["Name"])
#        print("\t" + "Plate type: " + stop["PlaceType"])

apiRequest = "https://reisapi.ruter.no/Travel/GetTravels?fromPlace=" + repr(originID) + "&toPlace=" + repr(destinationID) + "&isafter=true"

#apiRequest = "https://reisapi.ruter.no/Travel/GetTravels?fromPlace=" + repr(originID) + "&toPlace=" + repr(destinationID) + "&isafter=true&time=14062018070000&proposals=5"
response = requests.get(apiRequest)

print("Sending api request:" + apiRequest)

print("GET request status code: " + repr(response.status_code) + "\n")

if not response.content:
    print("Could not suggest any routes")
    exit()
else:
    print(response.content)

jsonData = json.loads(response.content)

print("showing results from " + origin + " to " + destination)

for proposal in jsonData:
    print(proposal)
    #print("\n")
    #print("Travel Time: " + proposal["TotalTravelTime"])
    #print("Departure Time: " + proposal["DepartureTime"])
    #print("Arrival Time: " + proposal["ArrivalTime"] + "\n")
    #print("------------------------------------------------")
