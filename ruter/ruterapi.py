import json, requests, urllib

class RuterApi:
    def __init__(self):
        print("initialized")

    def __repr__(self):
        return print("Hi there!")

    def __str__(self):
        return "ToSTring"

class Line:
    def __init__(self, json):
        self.ID = json["ID"]
        self.lineColor = json["LineColour"]
        self.name = json["Name"]
        self.transportation = json["Transportation"]

    def __str__(self):
        return "ID: {}, Name: {}, Transportation: {}".format(
                                        self.ID, self.name, self.transportation)

class Place:
    def __init__(self, json):
        self.district = json["District"]
        self.districtID = json["DistrictID"]
        self.ID = json["ID"]
        self.name = json["Name"]
        self.placeType = json["PlaceType"]
        if self.placeType == "Stop":
            self.isHub = json["IsHub"]
            self.lines = [Line(i) for i in json["Lines"]]
            self.shortName = json["ShortName"]
            self.x = json["X"]
            self.y = json["Y"]
            self.zone = json["Zone"]

    def __str__(self):
        if self.placeType == "Street":
            return "Name: {}, District: {}".format(
                    self.name, self.district)
        else:
            return "Name: {}, District: {}, Hub: {}, Zone: {}".format(
                    self.name, self.district, self.isHub, self.zone)

def get_place_suggestions(place):
    print("https://reisapi.ruter.no/Place/GetPlaces/?id="
                            + urllib.parse.quote_plus(place))
    response = requests.get("https://reisapi.ruter.no/Place/GetPlaces/?id="
                            + urllib.parse.quote_plus(place))
    if response.status_code == 200 and response.content:
        return [Place(i) for i in json.loads(response.content)]
    else:
        print("Status code: {} content: {}".format(response, response.content))
        return []
