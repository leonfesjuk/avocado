from resources.config import BASE_URL_FASTAPI, CONTROLLER_ID
from machine import Pin
import time
from resources.wificonnector import WifiConnection
from resources.requester import Request
import ujson as json
from resources.oled import oled_init, text_show_regular
from resources.moisture import MoistureSensor
from resources.reley import Relay
from resources.water_tank_fullness import Water_tank_fullness
from resources.timestamp_counter import get_time_and_update_rtc, get_iso_timestamp_from_rtc


def app_logic(
        min_fullness=20,
        max_fullness=100,
        min_moisture=60,
        max_moisture=80,
        water_pump_working_time=1, base_interval = 6000):

    send_data_url = BASE_URL_FASTAPI + "/post_data"
   
    
    #initialize timer
    last_run_base_foo = time.ticks_ms()

    #initialize  sensor/s
    moisture = MoistureSensor()
    water_tank_fullness_sensor = Water_tank_fullness()
    water_pump_relay = Relay()

    #initialize request client
    request_client = Request(url=send_data_url)
    

    if get_time_and_update_rtc():
        print("RTC synchronized successfully from FastAPI server.")
    else:
        print("Failed to synchronize RTC from FastAPI server. Using default/last known time.")
            

    #initial data
    data={}

    while True:

        current_time = time.ticks_ms()


        if time.ticks_diff(current_time, last_run_base_foo) > base_interval:
            
            data={}
            soil_moisture=moisture.moisture_get()
            data["controller_id"] = CONTROLLER_ID
            data["humidity"]=soil_moisture
            water_tank_fullness=water_tank_fullness_sensor.tank_fullnes()
            data["water_tank_fullness"]=water_tank_fullness
            data["water_pump_status"] = "off" 
            data["water_pump_working_time"] = 0 
            data["info"] = None 

            if water_tank_fullness > min_fullness and soil_moisture <= min_moisture:
                water_pump_relay.turn_on(water_pump_working_time)
                data["water_pump_status"]="on"
                data["water_pump_working_time"]=water_pump_working_time
                data["info"] = None
            elif water_tank_fullness < min_fullness:
                print("Water tank is empty, cannot turn on the pump.")
                data["info"] = "Water tank is empty, cannot turn on the pump."
                data["water_pump_status"]="off"
                data["water_pump_working_time"]=0
            elif soil_moisture >= max_moisture:
                data["water_pump_status"]="off"
                data["water_pump_working_time"]=0
                print("The soil is overmastered, check the pump")
            
            try:
                response = request_client.post(data=data)
                if response and response.status_code == 200:
                    print("Data sent successfully:", response.json())
                else:
                    print("Failed to send data or no response received.")
            except Exception as e:
                print("Error during POST request:", e)
            
            last_run_base_foo = current_time
        time.sleep_ms(100)





