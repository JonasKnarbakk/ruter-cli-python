import json, requests, urllib

class Line():
    def __init__(self, json):
        self.ID = json["ID"]
        self.lineColor = json["LineColour"]
        self.name = json["Name"]
        self.transportation = json["Transportation"]

    def __repr(self):
        return "Name: {}, Transportation: {}".format(
                self.name, self.transportation)

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

def get_place_suggestions(place):
    print("https://reisapi.ruter.no/Place/GetPlaces/?id="
                            + urllib.parse.quote_plus(place))
    response = requests.get("https://reisapi.ruter.no/Place/GetPlaces/?id="
                            + urllib.parse.quote_plus(place))
    if response.status_code == 200 and response.content:
        places = []
        for place in json.loads(response.content):
            if place["PlaceType"] == "Stop":
                places.append(Stop(place))
            elif place["PlaceType"] == "Area":
                places.append(Area(place))
            else:
                places.append(Place(place))
        return places
    else:
        print("Status code: {} content: {}".format(response, response.content))
        return []
