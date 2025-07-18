from machine import Pin, I2C
import time
from resources.VL53L0X import VL53L0X


class Water_tank_fullness():
    def __init__(self, scl_pin = 22, sda_pin=21, i2c_bus_id=0, i2c_baudrate=500000, min_fullnes=20, max_fullnes=5):
        self.scl_pin=scl_pin
        self.sda_pin=sda_pin
        self.i2c_bus_id=i2c_bus_id
        self.i2c_baudrate=i2c_baudrate
        self.min_fullnes=min_fullnes
        self.max_fullnes=max_fullnes
        self._initialize_i2c()
        self._initialize_vl53l0x_sensor()

    def _initialize_i2c(self):
        
        try:
            self.i2c = I2C(self.i2c_bus_id, 
                           scl=Pin(self.scl_pin), 
                           sda=Pin(self.sda_pin), 
                           freq=self.i2c_baudrate)
            print(f"I2C on {self.i2c_bus_id} initialized: "
                  f"SDA=GPIO{self.sda_pin}, SCL=GPIO{self.scl_pin}, Speed={self.i2c_baudrate} Gz")
        except Exception as e:
            raise RuntimeError(f"Initialization ERROR I2C: {e}. "
                               "Check connection.")
    
    def _initialize_vl53l0x_sensor(self):
      
        try:
            self.tof_sensor = VL53L0X(self.i2c)
            print(" VL53L0X Inizialized.")

            self.tof_sensor.set_measurement_timing_budget(50000)
            self.tof_sensor.set_Vcsel_pulse_period(self.tof_sensor.vcsel_period_type[0], 18)
            self.tof_sensor.set_Vcsel_pulse_period(self.tof_sensor.vcsel_period_type[1], 14)

        except Exception as e:
            raise RuntimeError(f"Initialization ERROR VL53L0X: {e}.")

    def read_distance_cm(self):
        
        if self.tof_sensor is None:
            print("Error: Sensor VL53L0X not initialized.")
            return None

        try:
            distance_mm = self.tof_sensor.read()
            if distance_mm is not None:
                return distance_mm / 10.0
            else:
                return None 
        except Exception as e:
            print(f"Reading distance ERROR: {e}")
            return None
        
    def tank_fullnes(self):
        try:
            distance = self.read_distance_cm()
            if distance is None:
                print("Distance reading Error")
            else:
                normalized_distance = (self.min_fullnes - distance) / (self.min_fullnes - self.max_fullnes)
                fullness_percentage = int(normalized_distance * 100)
                if fullness_percentage < 0:
                    return 0
                elif fullness_percentage > 100:
                    return 100
                else:
                    
                    return fullness_percentage
        except Exception as e:
            print(f"Fullness calculation Error: {e}")



