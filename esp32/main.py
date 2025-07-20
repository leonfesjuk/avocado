
from machine import Pin
import time
from resources.wificonnector import WifiConnection
from resources.requester import Request
import json
from resources.oled import oled_init, text_show_regular
from resources.moisture import MoistureSensor
from resources.reley import Relay
from resources.water_tank_fullness import Water_tank_fullness
from resources.timestamp_counter import get_time_and_update_rtc




while True:
    actual_time = get_time_and_update_rtc()
    print("Current time updated:", actual_time)

    time.sleep(5)  # Wait for 1 second before the next update