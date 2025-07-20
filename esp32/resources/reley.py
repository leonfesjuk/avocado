from machine import ADC, Pin
import time

class Relay:
    def __init__(self, pin=32):
        valid_relay_pins = [16, 17, 25, 26, 27, 32, 33]
        if pin not in valid_relay_pins:
            raise ValueError(f"Pin {pin} is not a valid or recommended pin for relay control on ESP32. "
                             f"Recommended: {valid_relay_pins}")
        self.pin = pin
        self.relay_pin = Pin(self.pin, Pin.OUT)
        

    def turn_on(self, work_time=1):
        self.relay_pin.value(1)
        print(f"Relay on pin {self.pin} is turned ON.")
        time.sleep(work_time)
        self.relay_pin.value(0)
        print(f"Relay on pin {self.pin} is turned OFF.")
            

