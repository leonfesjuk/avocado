
from machine import Pin
import time
from resources.wificonnector import WifiConnection
from resources.requester import Request
import json
from resources.oled import oled_init, text_show_regular
from resources.moisture import MoistureSensor
from resources.reley import Relay
from resources.water_tank_fullness import Water_tank_fullness





for _ in range(10):
    print(".", end="")
    time.sleep(0.5)

while True:

    tank_sensor = Water_tank_fullness()
    distance = tank_sensor.read_distance_cm()
    print(f"Distance is: {distance:.1f} sm")
    fullnes = tank_sensor.tank_fullnes()
    print(f"Fullnes: {fullnes}")

    time.sleep(0.5)

