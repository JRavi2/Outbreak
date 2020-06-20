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
    # l=['pharmacy','primary+health+care+center','goverment+hospitals']

    result = []
    for j in l:
        print(j)
        url = (
            "https://maps.googleapis.com/maps/api/place/textsearch/json?query="
            + str(j)
            + "&key=AIzaSyDRJfxExJoo1eMBj6T-pSEqpPO2o8W1Fes&location="
        )
        url += str(lati) + "," + str(longi)
        response = requests.get(url)
        data = response.json()
        destinations = []
        print(data)
        for i in range(20):
            lat = data["results"][i]["geometry"]["location"]["lat"]
            lng = data["results"][i]["geometry"]["location"]["lng"]
            destinations.append({"point": {"latitude": lat, "longitude": lng}})
        res = calc_dist(lati, longi, destinations)
        for i in range(20):
            result.append(
                {
                    "name": data["results"][i]["name"],
                    "address": data["results"][i]["formatted_address"],
                    "distance": res["matrix"][0][i]["response"]["routeSummary"][
                        "lengthInMeters"
                    ]
                    / 1000,
                }
            )
        # time.sleep(3)
    # print(result)
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
        if str(rows[i][0]).lower() == str(disease):
            # print("correctly found")
            # print(rows[i][1])
            if (
                (rows[i][1] == "acute")
                or (rows[i][1] == "acute/chronic")
                or (rows[i][1] == "chronic/acute")
            ):
                print("still correct")
                return find_place(lati, longi, ["clinic"])
            else:
                print("chronic one ")
                return find_place(lati, longi, ["hospital"])


# 28.6358749, 77.3738937, ['clinic']
# check("Adnexitis", 28.6358749, 77.3738937)
