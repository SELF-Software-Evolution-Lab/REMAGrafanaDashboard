import paho.mqtt.client as paho  # mqtt library
import os
import json
import time
import random
import csv
from geopy.geocoders import Nominatim
from datetime import datetime

ACCESS_TOKEN = 'bUdxXltNJd9c1NFS8MRV'  # Token of your device
broker = "thingsboard.cloud"  # host name
port = 1883  # data listening port
geolocator = Nominatim(user_agent='myapplication')
VARIABLE_TEMPERATURE = "temperature"
VARIABLE_HUMIDITY = "humidity"
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
                    build_payload(location, VARIABLE_HUMIDITY, row[4])
                else:
                    if location not in locations:
                        locations.append(location)
                    build_payload(location, VARIABLE_TEMPERATURE, row[4])
                    line_count += 1
        print(f'Processed {line_count} lines.')


def build_payload(Location_city, Variable_Taken, Value_Variable):
    payload = "{ \"%s\": %s}" % (Variable_Taken, Value_Variable)
    if len(locations) != 0 and Location_city == locations[0]:
        post_request(payload)


def post_request(payload):
    ret = client1.publish("v1/devices/me/telemetry", payload)
    print("Please check LATEST TELEMETRY field of your device")
    print("Return message from the server %s" % (ret))
    print(payload)


def main():
    connect()
    readCSV()


if __name__ == '__main__':
    main()
