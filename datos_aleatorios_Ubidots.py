import time
from tkinter.filedialog import Open
import requests
import csv
from geopy.geocoders import Nominatim

TOKEN = ""  # Put your TOKEN here
DEVICE_LABEL = ""  # Put your device label here
VARIABLE_TEMPERATURE_1 = "temperature"
VARIABLE_HUMIDITY_2 = "humidity"
VARIABLE_POSITION = "position"

geolocator = Nominatim(user_agent='myapplication')

# Variables CSV: Usuario, Ciudad, Fecha, Variable(humedad, temperatura), Medicion


def readCSV():
    with open('datos-historicos-iot.csv') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                location = geolocator.geocode(row[1])
                if row[3] == 'humedad':
                    build_payload(location, VARIABLE_HUMIDITY_2, row[4])
                else:
                    build_payload(location, VARIABLE_TEMPERATURE_1, row[4])
                    line_count += 1
        print(f'Processed {line_count} lines.')


def build_payload(Location_city, Variable_Taken, Value_Variable):
    payload = {
        VARIABLE_POSITION: {"value": 1, "context": {"lat": Location_city.latitude, "lng": Location_city.longitude}},
        Variable_Taken: Value_Variable,
    }

    print("[INFO] Attemping to send data")
    post_request(payload)
    print("[INFO] finished")


def post_request(payload):
    # Creates the headers for the HTTP requests
    url = "http://industrial.api.ubidots.com"
    url = "{}/api/v1.6/devices/{}".format(url, DEVICE_LABEL)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

    # Makes the HTTP requests
    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        req = requests.post(url=url, headers=headers, json=payload)
        status = req.status_code
        attempts += 1
        # time.sleep(1)

    # Processes results
    print(req.status_code, req.json())
    if status >= 400:
        print("[ERROR] Could not send data after 5 attempts, please check \
            your token credentials and internet connection")
        return False

    print("[INFO] request made properly, your device is updated")
    return True


def main():
    readCSV()


if __name__ == '__main__':
    while (True):
        main()
        time.sleep(1)
