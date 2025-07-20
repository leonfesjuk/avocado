import time
import network
import urequests
from resources.wificonnector import WifiConnection



class Request:
    def __init__(self , url = None):
        self.wifi_connector = WifiConnection()
        self.wlan_obj = network.WLAN(network.STA_IF)
        
        self.url = url

    def _ensure_wifi_connected(self):
        if self.wlan_obj.isconnected():
            print("Wi-Fi already connected ")
            return True
        else:
            print("Wi-Fi not connected. Starting connection...")
            return self.wifi_connector.connect_to_wifi()
        

    def get(self, url, headers=None):
      
        if not self._ensure_wifi_connected():
            return None 

        print(f"GET: {url}")
        response = None 
        try:
            response = urequests.get(url, headers=headers)
            print("Status GET", response.status_code)
            print("Included in request GET:")
            print(response.text)
            return response
        except Exception as e:
            print("GET error:", e)
            return None
        

    def post(self,  headers=None, data=None):
        
        if not self._ensure_wifi_connected():
            return None

        print(f" POST request start: {self.url}")
        response = None 
        try:
            
            if headers is None and data is not None:
                headers = {'Content-Type': 'application/json'}

            response = urequests.post(self.url, json=data, headers=headers)
            print("Satus POST request:", response.status_code)
            print("Request data POST:")
            if response.status_code == 200 and 'application/json' in response.headers.get('Content-Type', ''):
                print(response.json()) 
            else:
                print(response.text) 

            return response
        except Exception as e:
            print("Error POST:", e)
            return None
        finally:
            if response:
                response.close()
