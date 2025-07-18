from machine import ADC, Pin
import time

class MoistureSensor:
    def __init__(self, pin=36, calibration_dry=None, calibration_wet=None):
        valid_adc1_pins = [36, 39, 34, 35, 32, 33, 25, 26, 27, 14, 12]
        if pin not in valid_adc1_pins:
            raise ValueError(f"Pin {pin} is not a valid or recommended ADC1 pin on ESP32. "
                             f"Recommended: {valid_adc1_pins}")

        self.pin = pin
        self.adc_pin = ADC(Pin(self.pin))

        self.adc_pin.atten(ADC.ATTN_11DB)
        self.adc_pin.width(ADC.WIDTH_12BIT)

        self.calibration_dry = calibration_dry if calibration_dry is not None else 56454
        self.calibration_wet = calibration_wet if calibration_wet is not None else 24886
        
        if self.calibration_dry <= self.calibration_wet:
            print("Warning: For a resistive sensor, 'calibration_dry' should be greater than 'calibration_wet'.")
            print("Please ensure your calibration values are correct.")


    def read_raw(self):
        return self.adc_pin.read_u16()

    def _moisture_to_percentage(self, raw_value):
        
        if raw_value >= self.calibration_dry:
            return 0.0
        elif raw_value <= self.calibration_wet:
            return 100.0
        
        value_range = self.calibration_dry - self.calibration_wet
        if value_range == 0:
            print("Error: Calibration dry and wet values are the same. Cannot calculate percentage.")
            return 0.0

        moisture_scaled = (self.calibration_dry - raw_value) / value_range
        
        percentage = max(0.0, min(100.0, moisture_scaled * 100.0))
        return percentage

    def moisture_get(self, num_samples=5):
        if num_samples <= 0:
            raise ValueError("Number of samples must be positive.")

        sensor_readings_percentage = []
        
        for _ in range(num_samples):
            raw_val = self.read_raw()
            percentage = self._moisture_to_percentage(raw_val)
            sensor_readings_percentage.append(percentage)
            time.sleep_ms(50)

        if not sensor_readings_percentage:
            return 0.0
            
        return sum(sensor_readings_percentage) / len(sensor_readings_percentage)
