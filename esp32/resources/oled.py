from machine import Pin, I2C
import time
import resources.ssd1306 as ssd1306

def oled_init(bus_id=0, scl_pin=22, sda_pin=21, freq=400000, width=128, height=64, contrast=150):
    i2c = I2C(bus_id, scl=Pin(scl_pin), sda=Pin(sda_pin), freq=freq)
    print("Scanning I2C bus...")
    devices = i2c.scan()

    if not devices:
        print("No I2C devices found!")
        print("Check wiring (SDA=GP16/Pin 21, SCL=GP17/Pin 22), and power (VCC to 3V3(OUT)/Pin 36, GND).")
        
    else:
        print("I2C devices found at addresses:", [hex(device) for device in devices])

    WIDTH = width
    HEIGHT = height
    oled = None

   
    initialization_attempts = [
        {'addr': 0x3C, 'external_vcc': False, 'msg': "0x3C (external_vcc=False)"},
        {'addr': 0x3C, 'external_vcc': True, 'msg': "0x3C (external_vcc=True)"},
        {'addr': 0x3D, 'external_vcc': False, 'msg': "0x3D (external_vcc=False)"},
        {'addr': 0x3D, 'external_vcc': True, 'msg': "0x3D (external_vcc=True)"},
    ]

    for attempt in initialization_attempts:
        try:
            oled = ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=attempt['addr'], external_vcc=attempt['external_vcc'])
            print(f"OLED initialized successfully with address {attempt['msg']}.")
            break 
        except Exception as e:
            print(f"Error initializing OLED with {attempt['msg']}: {e}")
            oled = None 

    
    if oled is None:
        print("Could not initialize OLED after multiple attempts. Check connections, power, and driver IC compatibility (SSD1315).")
        return None

   
    oled.contrast(contrast) 
    oled.poweron()          
    oled.fill(0)          
    oled.show()             
    print("Display settings applied (contrast, poweron) and display cleared.")

    return oled 


def text_show_regular(oled_obj, text_to_display, x_position, y_position):
    oled_obj.fill(0)
    oled_obj.text(text_to_display, x_position, y_position)
    oled_obj.show()
    print(f"Displayed text: '{text_to_display}' at ({x_position}, {y_position})")