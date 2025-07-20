import utime
import time
import network
import urequests
from resources.wificonnector import WifiConnection
from machine import RTC
import ujson
from resources.requester import Request
from resources.config import BASE_URL_FASTAPI

TIMESTAMP_URL = BASE_URL_FASTAPI + "/get_time"

rtc = RTC()

def get_time_and_update_rtc():
    request_client = Request() 

    response = None
    try:
        response = request_client.get(TIMESTAMP_URL)

        if response:
            if response.status_code == 200:
                try:
                    data = ujson.loads(response.text) 
                    if all(k in data for k in ['year', 'month', 'day', 'hour', 'minute', 'second']):
                        year = data['year']
                        month = data['month']
                        day = data['day']
                        hour = data['hour']
                        minute = data['minute']
                        second = data['second']
                        
                        rtc.datetime((year, month, day, 0, hour, minute, second, 0))
                        print(f"RTC updated to: {year}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}:{second:02d}")
                        return True
                    else:
                        print("Error: Incomplete time data received from server.")
                        return False
                except ValueError as ve:
                    print(f"Error parsing JSON response for time: {ve}")
                    return False
            else:
                print(f"Error: Server returned status code {response.status_code} for time sync.")
                return False
        else:
            print("Error: No response received from server for time sync.")
            return False
    except Exception as e:
        print(f"Error during time synchronization request: {e}")
        return False
    finally:
        try:
            if response:
                response.close()
        except Exception as e:
            print("Error closing response (custom):", e)
                

def get_iso_timestamp_from_rtc():
    t = utime.localtime()

    if t[0] < 2020:
        print("Warning: RTC time appears to be uninitialized or incorrect (year < 2020).")
        return None 
    
    timestamp_str = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
        t[0], t[1], t[2], t[3], t[4], t[5]
    )
    return timestamp_str
