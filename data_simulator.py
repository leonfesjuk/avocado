import requests
import time
import random
from datetime import datetime, timedelta

# --- Configuration ---
# Make sure your FastAPI server is running and accessible at this URL
BASE_URL = "https://avocado-1-arvi.onrender.com" 
# Use the same controller ID as your ESP32 config
CONTROLLER_ID = 1 

SEND_DATA_URL = f"{BASE_URL}/post_data"

# Simulation parameters
SIMULATED_DAYS = 3
DATA_INTERVAL_HOURS = 2  # Send data every 2 simulated hours
TOTAL_DATA_POINTS = (SIMULATED_DAYS * 24) // DATA_INTERVAL_HOURS

# Moisture simulation parameters
MIN_MOISTURE = 60
MAX_MOISTURE = 80
DRYING_RATE = 1.5  # How many % moisture drops per interval

def run_simulator():
    """
    Simulates an ESP32 controller sending data to the backend.
    """
    print(f"Starting data simulator for {SIMULATED_DAYS} simulated days...")
    print(f"Sending data to {SEND_DATA_URL}")

    # Initial state
    current_humidity = MAX_MOISTURE
    current_tank_fullness = 90
    simulated_time = datetime.now()

    for i in range(TOTAL_DATA_POINTS):
        data = {
            "controller_id": CONTROLLER_ID,
            "humidity": int(current_humidity),
            "water_tank_fullness": current_tank_fullness,
            "water_pump_status": "off",
            "water_pump_working_time": 0,
            "info": "Simulated data"
        }

        # --- Simulate watering logic ---
        if current_humidity <= MIN_MOISTURE:
            print(f"\n--- SIMULATING WATERING (Humidity: {current_humidity:.1f}%) ---")
            data["water_pump_status"] = "on"
            data["water_pump_working_time"] = 1
            current_humidity = MAX_MOISTURE  # Reset humidity after watering
            print(f"--- WATERING COMPLETE (New Humidity: {current_humidity:.1f}%) ---\n")
        
        # --- Send data to backend ---
        try:
            # We override the timestamp in the backend, but we send it for completeness
            # In a real scenario, the ESP32 would get the time from the server
            
            print(f"Simulated Time: {simulated_time.strftime('%Y-%m-%d %H:%M:%S')}, Sending data: {data}")
            
            response = requests.post(SEND_DATA_URL, json=data)
            response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx) 
            
            print(f"-> Success: Server responded with {response.status_code}\n")

        except requests.exceptions.RequestException as e:
            print(f"\n--- ERROR: Could not connect to the server at {BASE_URL} ---")
            print("Please make sure your FastAPI backend server is running.")
            print(f"Error details: {e}")
            return  # Stop the script if the server is not available

        # --- Update state for next iteration ---
        # Decrease humidity to simulate drying
        current_humidity -= DRYING_RATE + random.uniform(-0.5, 0.5)
        # Advance time
        simulated_time += timedelta(hours=DATA_INTERVAL_HOURS)
        
        # Wait a little bit to not overwhelm the server and to see the output
        time.sleep(1)

    print("Data simulation complete.")

if __name__ == "__main__":
    run_simulator()
