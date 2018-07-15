import json, requests, urllib
from datetime import datetime

transportMethods = {    0 : "🚶",
                        1 : "",
                        2 : "🚌",
                        3 : "",
                        4 : "",
                        5 : "",
                        6 : "🚆",
                        7 : "🚊",
                        8 : "🚇" }

def format_time(string):
    return datetime.strptime(string, "%Y-%m-%dT%H:%M:%S+02:00").strftime("\033[33m%H:%M:%S\033[0m")

class Point():
    def __init__(self, json):
        self.x = json["X"]
        self.y = json["Y"]

    def __str__(self):
        return "{},{}".format(self.x, self.y)

class Line():
    def __init__(self, json):
        self.ID = json["ID"]
        self.lineColor = json["LineColour"]
        self.name = json["Name"]
        self.transportation = json["Transportation"]

    def __str__(self):
        return "ID: {}, Name: {}, Transportation: {}".format(
        self.ID, self.name, self.transportation)

class Place(object):
    def __init__(self, json):
        self.district = json["District"]
        self.districtID = json["DistrictID"]
        self.ID = json["ID"]
        self.name = json["Name"]
        self.placeType = json["PlaceType"]

    def __str__(self):
            return "Name: {}, District: {}".format(self.name, self.district)

class Stop(Place):
    def __init__(self, json):
        super(Stop, self).__init__(json)
        self.isHub = json["IsHub"]
        self.lines = [Line(i) for i in json["Lines"]]
        self.shortName = json["ShortName"]
        self.x = json["X"]
        self.y = json["Y"]
        self.zone = json["Zone"]

    def __str__(self):
        return super(Stop, self).__str__() \
                + " Is Hub: {}, Lines: {}, Zone: {}".format(
                                                        self.name,
                                                        self.district,
                                                        self.isHub,
                                                        len(self.lines),
                                                        self.zone)

class Area(Place):
    def __init__(self, json):
        super(Area, self).__init__(json)
        self.center = { "X" : json["Center"]["X"],
                        "Y" : json["Center"]["Y"]}
        self.stops = [Stop(i) for i in json["Stops"]]

    def __str__(self):
        return super(Area, self).__str__() + " Center: X({}) Y({}), Stops: {}" \
                .format(self.center["X"], self.center["Y"], len(self.stops))

class Stage():
    def __init__(self, json):
        self.arrivalTime = json["ArrivalTime"]
        self.departureTime = json["DepartureTime"]
        self.geometry = json["Geometry"]
        self.transportation = json["Transportation"]

    def __str__(self):
        return "Arrival: {}, Departure: {}, Transportation: {}".format(
                self.arrivalTime, self.departureTime, self.transportation)

class WalkingStage(Stage):
    def __init__(self, json):
        super(WalkingStage, self).__init__(json)
        self.walkingTime = json["WalkingTime"]
        self.arrivalPoint = Point(json["ArrivalPoint"])
        self.departurePoint = Point(json["DeparturePoint"])

    def __str__(self):
        return "[{}] {} {} [{}] {}".format(format_time(self.departureTime),
                                    self.departurePoint,
                                    transportMethods[self.transportation],
                                    format_time(self.arrivalTime),
                                    self.arrivalPoint)

class TravelStage(Stage):
    def __init__(self, json):
        super(TravelStage, self).__init__(json)
        self.arrivalDelay = json["ArrivalDelay"]
        self.departureDelay = json["DepartureDelay"]
        self.arrivalStop = Stop(json["ArrivalStop"])
        self.departureStop = Stop(json["DepartureStop"])
        self.destination = json["Destination"]
        self.intermediateStops = json["IntermediateStops"]
        self.lineColor = json["LineColour"]
        self.lineID = json["LineID"]
        self.lineName = json["LineName"]
        self.monitored = json["Monitored"]
        self.operator = json["Operator"]
        self.remarks = json["Remarks"]
        self.tourID = json["TourID"]
        self.tourLineID = json["TourLineID"]

    def __str__(self):
        return "[{}] {} {} [{}] {}".format(format_time(self.departureTime),
                                    self.departureStop.name,
                                    transportMethods[self.transportation],
                                    format_time(self.arrivalTime),
                                    self.arrivalStop.name)

class TravelProposal():
    def __init__(self, json):
        self.arrivalTime = json["ArrivalTime"]
        self.departureTime = json["DepartureTime"]
        self.stages = get_stages_from_json(json["Stages"])
        self.totalTravelTime = json["TotalTravelTime"]
        self.zones = json["Zones"]

    def __str__(self):
        return "Departure: {}, Total Travel: {}, Arrival: {}, Stages: {}, ".format(
                self.departureTime, self.totalTravelTime, self.arrivalTime, \
                        len(self.stages))

def get_stages_from_json(json):
    stages = []
    for stage in json:
        if "ArrivalPoint" in stage:
            stages.append(WalkingStage(stage))
        elif "ArrivalStop" in stage:
            stages.append(TravelStage(stage))

    return stages

def get_place_suggestions(place):
    response = requests.get("https://reisapi.ruter.no/Place/GetPlaces/?id="
                            + urllib.parse.quote_plus(place))
    if response.status_code == 200 and response.content:
        places = []
        for place in response.json():
            if place["PlaceType"] == "Stop":
                places.append(Stop(place))
            elif place["PlaceType"] == "Area":
                places.append(Area(place))
            else:
                places.append(Place(place))
        return places
    else:
        print("Status code: {} content: {}".format(response.status_code, response.content))
        return []

def get_stop_suggestions(place):
    response = requests.get("https://reisapi.ruter.no/Place/GetPlaces/?id="
                            + urllib.parse.quote_plus(place))
    if response.status_code == 200 and response.content:
        places = []
        for place in response.json():
            if place["PlaceType"] == "Stop":
                places.append(Stop(place))

        return places
    else:
        print("Status code: {} content: {}".format(response.status_code, response.content))
        return []

def get_travel_suggestions(origin, destination, isAfter):
    #  print("https://reisapi.ruter.no/Travel/GetTravels?" \
            #  + "fromPlace=" + urllib.parse.quote_plus(str(origin)) \
            #  + "&toPlace=" + urllib.parse.quote_plus(str(destination)) \
            #  + "&isafter=" + isAfter)
    response = requests.get("https://reisapi.ruter.no/Travel/GetTravels?" \
            + "fromPlace=" + urllib.parse.quote_plus(str(origin)) \
            + "&toPlace=" + urllib.parse.quote_plus(str(destination)) \
            + "&isafter=" + isAfter)

    if response.status_code == 200 and response.content:
        travelSuggestions = response.json()
        if not travelSuggestions["ReisError"]:
            travels = []
            for travel in response.json()["TravelProposals"]:
                travels.append(TravelProposal(travel))
            return travels
        else:
            print(travelSuggestions["ReisError"])
            return []
    else:
        if response.content["ReisError"]:
            print(response.content["ReisError"])
        print("Statis code: {} content: {}".format(response.status_code, response.content))
        return []
