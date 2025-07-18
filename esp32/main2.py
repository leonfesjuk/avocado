
from machine import Pin
import time
from resources.wificonnector import WifiConnection
from resources.requester import Request
import json
from resources.oled import oled_init, text_show_regular
from resources.moisture import MoistureSensor
from resources.reley import Relay
from resources.water_tank_fullness import Water_tank_fullness





data = {
    "name": "names",
    "value": 123
}

#my_oled = oled_init(contrast=255)
#text_show_regular(my_oled, str("test"), 0, 0)

print(data)

url = "https://webhook.site/5230d868-33ce-4b97-8944-f6abfa98e1bb"

my_request_handler = Request(data=data, url=url)
response_from_post = my_request_handler.post()

if response_from_post:
    print(f"POST Response Status Code: {response_from_post.status_code}")

    
    print("Response Headers:")
    for header, value in response_from_post.headers.items():
        print(f"  {header}: {value}")

    content_type = response_from_post.headers.get('Content-Type', '')
    if 'application/json' in content_type:
        try:
            print("\nResponse Body (JSON):")
            print(response_from_post.json())
        except ValueError:
            print("\nResponse Body (Raw Text - JSON parse failed):")
            print(response_from_post.text)
    else:
        print("\nResponse Body (Text):")
        

 
else:
    print("Failed to get a POST response. Check logs above for Wi-Fi or request errors.")

print("\n--- Script finished. ---")

print("sleepinf=g")
time.sleep(2)

relay_1 = Relay()
tank_sensor = Water_tank_fullness()
distance = tank_sensor.read_distance_cm()
print(f"Distance is: {distance:.1f} sm")
time.sleep(0.5)

