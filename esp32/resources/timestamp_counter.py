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

rtc = RTC()

def get_time_and_update_rtc():
    request_client = Request()
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
