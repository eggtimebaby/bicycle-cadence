# hardware.py
from machine import Pin, I2C, Timer
from ssd1306 import SSD1306_I2C
import config
import time

class HardwareManager:
    def __init__(self):
        self.initialized = False
        self.error_code = None
        
    def initialize(self):
        """Initialize all hardware components with error handling"""
        try:
            # Initialize I2C and OLED
            self.i2c = I2C(0, sda=Pin(config.PIN_SDA), scl=Pin(config.PIN_SCL))
            self.oled = SSD1306_I2C(config.OLED_WIDTH, config.OLED_HEIGHT, self.i2c, addr=config.OLED_ADDR)
            
            # Initialize external LED
            self.led = Pin(13, Pin.OUT)  # Changed to GP13
            
            # Initialize Reed Switch with pull-up
            self.reed_switch = Pin(config.PIN_REED_SWITCH, Pin.IN, Pin.PULL_UP)
            
            # Initialize Button with pull-up
            self.button = Pin(config.PIN_BUTTON, Pin.IN, Pin.PULL_UP)
            
            # Set initialization flag
            self.initialized = True
            return True
            
        except Exception as e:
            self.error_code = config.ERR_HARDWARE_INIT
            print(f"Hardware initialization failed: {str(e)}")
            return False
    
    def diagnostic_check(self):
        """Run diagnostic checks on all hardware components"""
        if not self.initialized:
            return False, "Hardware not initialized"
            
        diagnostics = {
            "i2c": False,
            "oled": False,
            "reed_switch": False,
            "button": False,
            "led": False
        }
        
        try:
            # Check I2C
            devices = self.i2c.scan()
            diagnostics["i2c"] = config.OLED_ADDR in devices
            
            # Check OLED
            self.oled.fill(0)
            self.oled.text("Test", 0, 0)
            self.oled.show()
            diagnostics["oled"] = True
            
            # Check LED
            self.led.on()
            time.sleep_ms(100)
            self.led.off()
            diagnostics["led"] = True
            
            # Check Reed Switch and Button (can only verify they're readable)
            self.reed_switch.value()
            diagnostics["reed_switch"] = True
            
            self.button.value()
            diagnostics["button"] = True
            
        except Exception as e:
            print(f"Diagnostic check failed: {str(e)}")
            
        return all(diagnostics.values()), diagnostics
    
    def cleanup(self):
        """Cleanup hardware resources"""
        if self.initialized:
            self.led.off()
            self.oled.fill(0)
            self.oled.show()