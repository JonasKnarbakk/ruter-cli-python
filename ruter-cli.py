#!/usr/bin/env python3

import json, requests, urllib

# Estimate the time i will arrive at work using the ruter API
# ruterDate=$(echo ${leftDate}${leftTime} | sed 's/://g;s/-//g')
# estimatedArrival=$(curl -i -s -N -X GET http://reisapi.ruter.no/Travel/GetTravels\?fromPlace\=3011036\&toPlace\=3010445\&isAfter\=true\&time\=${ruterDate}

response = requests.get("http://reisapi.ruter.no/Travel/GetTravels?fromPlace=3011036&toPlace=3010445&isAfter=true")

print("GET request status code: " + repr(response.status_code) + "\n")

jsonData = json.loads(response.content)

origin = "Marmorveien 9 (Oslo)"

apiGetPlaceString = "http://reisapi.ruter.no/Place/GetPlaces/?id=" + urllib.parse.quote_plus(origin)

print("Using api string: " + apiGetPlaceString)

response = requests.get(apiGetPlaceString)

print("GET request status code: " + repr(response.status_code) + "\n")

jsonDataStops = json.loads(response.content)

#print(jsonDataStops)
#print("Stops:")
print("\t" + "Name: " + jsonDataStops[0]["Name"])
print("\t" + "Plate type: " + jsonDataStops[0]["PlaceType"])
#for stop in jsonDataStops:
#    if(stop["District"] == "Oslo" and stop["PlaceType"] == "Stop"):
#        print("\t" + "Name: " + stop["Name"])
#        print("\t" + "Plate type: " + stop["PlaceType"])

print("Showing results from " + " to ")

for proposal in jsonData["TravelProposals"]:
    print("\n")
    print("Travel Time: " + proposal["TotalTravelTime"])
    print("Departure Time: " + proposal["DepartureTime"])
    print("Arrival Time: " + proposal["ArrivalTime"] + "\n")
    print("------------------------------------------------")
    
