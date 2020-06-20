import requests
import json
import csv
import time
import os
import operator


def calc_dist(lat, long, destinations):
    request_body = {
        "origins": [{"point": {"latitude": lat, "longitude": long}}],
        "destinations": destinations,
    }

    header = {"Content-Type": "application/json"}

    jsonData = json.dumps(request_body)

    res = requests.post(
        "https://api.tomtom.com/routing/1/matrix/sync/json?key=2hvVqQig2YrGgunrjXUNJiaWXAGCEHg9&routeType=fastest&travelMode=car",
        data=jsonData,
        headers=header,
    )
    res = res.json()
    return res


def find_place(lati, longi, l):
    result = []
    for j in l:
        print(j)
        url = (
            "https://api.mapbox.com/geocoding/v5/mapbox.places/"
            + str(j)
            + ".json?country=in&proximity="
            + str(longi)
            + ","
            + str(lati)
            + "&limit=20&access_token=pk.eyJ1Ijoib2xkbW9uayIsImEiOiJja2Jua2o1OHQwN3g4MnBwbm1sZGIzd3MyIn0.5Az8PsHtt4Gp6SlanOUv6Q"
        )
        response = requests.get(url)
        data = response.json()
        destinations = []
        for i in range(len(data["features"])):
            lat = data["features"][i]["geometry"]["coordinates"][1]
            lng = data["features"][i]["geometry"]["coordinates"][0]
            destinations.append({"point": {"latitude": lat, "longitude": lng}})
        res = calc_dist(lati, longi, destinations)
        for i in range(len(data["features"])):
            result.append(
                {
                    "name": data["features"][i]["text"],
                    "address": data["features"][i]["place_name"],
                    "distance": res["matrix"][0][i]["response"]["routeSummary"][
                        "lengthInMeters"
                    ]
                    / 1000,
                }
            )
    result.sort(key=operator.itemgetter("distance"))
    return result


def check(disease, lati, longi):
    rows = []

    filename = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "list_hospital/diseases.csv"
    )
    # filename='/home/kartik/Desktop/outbreak/list__hospital/diseases.csv'
    with open(filename, "r") as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            rows.append(row)

    for i in range(0, len(rows), 2):
        if str(disease).lower() in str(rows[i][0]).lower():
            if (
                (rows[i][1] == "acute")
                or (rows[i][1] == "acute/chronic")
                or (rows[i][1] == "chronic/acute")
            ):
                return find_place(lati, longi, ["pharmacy"])
            else:
                return find_place(lati, longi, ["hospital"])


# 28.6358749, 77.3738937, ['clinic']
# check("Adnexitis", 28.6358749, 77.3738937)
