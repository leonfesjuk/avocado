from os import utime
import time
import network
import urequests
from resources.wificonnector import WifiConnection
from machine import RTC
import json 
from resources.requester import Request
from resources.config import BASE_URL_FASTAPI

TIMESTAMP_URL = BASE_URL_FASTAPI + "/get_time"


rtc = RTC()

def get_time_and_update_rtc():
    request_client = Request()
    try:
        response = request_client.get(TIMESTAMP_URL)

        if response:
            if response.status_code == 200:
                try:
                    data = response.json()
                    if all(k in data for k in ['year', 'month', 'day', 'hour', 'minute', 'second']):
                        year = data['year']
                        month = data['month']
                        day = data['day']
                        hour = data['hour']
                        minute = data['minute']
                        second = data['second']
                        rtc.datetime((year, month, day, 0, hour, minute, second, 0))
                        return True
                    else:
                        return False
                except ValueError:
                    return False
            else:
                return False
        else:
            return False
    finally:
            if response:
                response.close() 

def get_iso_timestamp_from_rtc():
    t = utime.localtime()

    if t[0] < 2020:
        return None
    
    timestamp_str = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
        t[0], t[1], t[2], t[3], t[4], t[5]
    )
    return timestamp_str