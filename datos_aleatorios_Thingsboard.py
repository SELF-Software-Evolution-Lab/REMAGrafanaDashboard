import paho.mqtt.client as paho  # mqtt library
import os
import json
import time
import random
import csv
from geopy.geocoders import Nominatim
from datetime import datetime

ACCESS_TOKEN = 'HIseKlNQFsCCc0zcHK14'  # Token of your device
ACCESS_TOKEN_2 = 'dapWd3YFZg3jwLgRxCEI'  # Token of your device
broker = "demo.thingsboard.io"  # host name
port = 1883  # data listening port
geolocator = Nominatim(user_agent='myapplication')
VARIABLE_TEMPERATURE_1 = "temperature"
VARIABLE_HUMIDITY_2 = "humidity"
VARIABLE_POSITION = "position"
client1 = paho.Client("control1")  # create client object
locations = []


def on_publish(client, userdata, result):  # create function for callback
    print("data published to thingsboard \n")
    pass


def connect():
    client1.on_publish = on_publish  # assign function to callback
    # access token from thingsboard device
    client1.username_pw_set(ACCESS_TOKEN)
    client1.connect(broker, port, keepalive=60)  # establish connection
    print(client1.is_connected)


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
                    if location not in locations:
                        locations.append(location)
                    build_payload(location, VARIABLE_TEMPERATURE_1, row[4])
                    line_count += 1
        print(f'Processed {line_count} lines.')


def build_payload(Location_city, Variable_Taken, Value_Variable):
    # payload = "{ \"%s\": %s, \"latitude\": %s, \"longitude\": %s}" % (
    #     Variable_Taken, Value_Variable, Location_city.latitude, Location_city.longitude)
    print(Location_city.latitude, Location_city.longitude)
    payload = "{ \"%s\": %s}" % (Variable_Taken, Value_Variable)
    print(payload)
    if len(locations) != 0 and Location_city == locations[0]:
        post_request(payload)


def post_request(payload):
    ret = client1.publish("v1/devices/me/telemetry", payload)
    print("Please check LATEST TELEMETRY field of your device")
    print("Return message from the server %s" % (ret))
    print(payload)
    # time.sleep(5)


def main():
    connect()
    readCSV()


if __name__ == '__main__':
    main()
