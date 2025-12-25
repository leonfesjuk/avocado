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
        water_pump_working_time=1):

    send_data_url = BASE_URL_FASTAPI + "/post_data"
    
    # Timings in milliseconds
    CHECK_INTERVAL = 20 * 60 * 1000  # 20 minutes
    LOG_INTERVAL_COUNT = 6  # Log every 6th check (6 * 20 min = 2 hours)

    # State variables
    last_check_time = time.ticks_ms()
    check_counter = 0

    # Initialize sensors and relay
    moisture = MoistureSensor()
    water_tank_fullness_sensor = Water_tank_fullness()
    water_pump_relay = Relay()

    # Initialize request client
    request_client = Request(url=send_data_url)
    
    if get_time_and_update_rtc():
        print("RTC synchronized successfully from FastAPI server.")
    else:
        print("Failed to synchronize RTC from FastAPI server. Using default/last known time.")
            
    while True:
        try:
            current_time = time.ticks_ms()

            # --- Main 20-minute check cycle ---
            if time.ticks_diff(current_time, last_check_time) > CHECK_INTERVAL:
                last_check_time = current_time
                check_counter += 1
                
                data = {}
                soil_moisture = moisture.moisture_get()
                water_tank_fullness = water_tank_fullness_sensor.tank_fullnes()
                
                data["controller_id"] = CONTROLLER_ID
                data["humidity"] = soil_moisture
                data["water_tank_fullness"] = water_tank_fullness
                data["water_pump_status"] = "off" 
                data["water_pump_working_time"] = 0 
                data["info"] = None 

                should_log_data = False

                # --- Watering Logic ---
                if water_tank_fullness > min_fullness and soil_moisture <= min_moisture:
                    water_pump_relay.turn_on(water_pump_working_time)
                    data["water_pump_status"] = "on"
                    data["water_pump_working_time"] = water_pump_working_time
                    print("Water pump activated.")
                    should_log_data = True  # Log data immediately after watering
                
                elif water_tank_fullness < min_fullness:
                    data["info"] = "Water tank is empty, cannot turn on the pump."
                    print(data["info"])
                
                elif soil_moisture >= max_moisture:
                    data["info"] = "The soil is over-moistured, check the pump"
                    print(data["info"])
                
                # --- Data Logging Logic ---
                if check_counter >= LOG_INTERVAL_COUNT:
                    should_log_data = True
                    check_counter = 0  # Reset counter

                if should_log_data:
                    print("Sending data to server...")
                    response = request_client.post(data=data)
                    if response and response.status_code == 200:
                        print("Data sent successfully:", response.json())
                    else:
                        print("Failed to send data or no response received.")
                else:
                    print(f"Check completed. Soil moisture: {soil_moisture}%. Tank fullness: {water_tank_fullness}%. No data sent.")

            # Sleep for a short time to keep the loop from running too fast
            time.sleep(1)

        except Exception as e:
            print("An error occurred in the main loop:", e)
            # Wait a bit before retrying to avoid rapid failure loops
            time.sleep(60)





