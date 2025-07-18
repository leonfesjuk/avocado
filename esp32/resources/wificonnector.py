import network
import time
#from config import 

WIFI_SSID = "Redmi Note 13"
WIFI_PASSWORD = "MetalisT"

class WifiConnection:
    def __init__(self, wifi_pass = WIFI_PASSWORD, wifi_ssid = WIFI_SSID):
        self.wifi_pass=wifi_pass
        self.wifi_ssid=wifi_ssid

    def connect_to_wifi(self):
        
        sta_if = network.WLAN(network.STA_IF)
        
        if not sta_if.active():
            sta_if.active(True)

        sta_if.disconnect()
        time.sleep(1)


        sta_if.connect(self.wifi_ssid, self.wifi_pass)

        max_attempts = 10

        while not sta_if.isconnected() and sta_if.status() != network.STAT_NO_AP_FOUND:
            print(".", end="")
            time.sleep(0.5)
            max_attempts -= 1
            if max_attempts <= 0:
                print("\n Cant connect tp WI-FI")
                return False
            
        if sta_if.isconnected():
            print("\n NodeMCU conected to WI-WI!")
            info = sta_if.ifconfig()
            print(f"WI-FI config {info}")
            time.sleep(1)
            print(f"WI-FI config {info}")
            time.sleep(1)
            print(f"WI-FI config {info}")
            return True
        elif sta_if.status() == network.STAT_NO_AP_FOUND:
            print(f"\n ERROR: WI-FI SSID {self.wifi_ssid} not founded")
            return False
        else:
            print("\n Connection ERROR")
            return False