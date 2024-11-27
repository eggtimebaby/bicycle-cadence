# main.py
from machine import Pin, Timer, deepsleep
import time
import config
from hardware import HardwareManager
from rpm_calc import RPMCalculator
from button_handler import ButtonHandler

class CadenceSensor:
    def __init__(self):
        self.hw = HardwareManager()
        self.rpm_calc = RPMCalculator()
        self.button_handler = ButtonHandler()
        self.last_display_update = 0
        self.last_trigger_time = 0
        
    def initialize(self):
        """Initialize the system and run diagnostics"""
        if not self.hw.initialize():
            print("Hardware initialization failed!")
            return False
            
        # Run diagnostic check
        success, diagnostics = self.hw.diagnostic_check()
        if not success:
            print("Diagnostic check failed:", diagnostics)
            return False
            
        # Setup interrupts
        self.hw.reed_switch.irq(trigger=Pin.IRQ_FALLING, handler=self._reed_switch_callback)
        self.hw.button.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self._button_callback)
        
        return True
        
    def _reed_switch_callback(self, pin):
        """Handle reed switch triggers with LED flash and debouncing"""
        try:
            current_time = time.ticks_ms()
            
            # If in sleep mode, ignore triggers
            if self.button_handler.get_sleep_mode():
                return
                
            # Check if enough time has passed since last trigger
            if time.ticks_diff(current_time, self.last_trigger_time) < config.REED_SWITCH_DEAD_TIME:
                return
                
            self.last_trigger_time = current_time
            self.rpm_calc.add_trigger()
            
            # Flash LED
            self.hw.led.on()
            time.sleep_ms(50)
            self.hw.led.off()
            
        except Exception as e:
            print(f"Reed switch error: {str(e)}")
            
    def _button_callback(self, pin):
        """Handle button events"""
        try:
            event = self.button_handler.handle_press(pin.value())
            
            if event == "LONG_PRESS":
                self.rpm_calc.reset()
                
            elif event == "TOGGLE_SLEEP":
                if self.button_handler.get_sleep_mode():
                    # Enter deep sleep
                    self.hw.cleanup()
                    print("Entering deep sleep...")
                    deepsleep()
                else:
                    # Wake up actions
                    self.rpm_calc.reset()
                    
        except Exception as e:
            print(f"Button handler error: {str(e)}")
            
    def _update_display(self):
        """Update OLED display"""
        try:
            # Clear display
            self.hw.oled.fill(0)
            
            # Display session time at top
            mins, secs = self.rpm_calc.get_session_time()
            self.hw.oled.text(f"Time: {mins:02d}:{secs:02d}", 0, 0)
            
            # Display rotation count
            self.hw.oled.text("Rotations:", 0, 24)
            self.hw.oled.text(str(self.rpm_calc.total_triggers), 0, 40)
            
            # Show sleep mode status
            if self.button_handler.get_sleep_mode():
                self.hw.oled.text("SLEEP PENDING", 0, 56)
                
            self.hw.oled.show()
            
        except Exception as e:
            print(f"Display update error: {str(e)}")
            
    def run(self):
        """Main program loop"""
        print("Starting cadence sensor...")
        
        while True:
            try:
                current_time = time.ticks_ms()
                
                # Update display at refresh rate
                if time.ticks_diff(current_time, self.last_display_update) >= config.DISPLAY_REFRESH_MS:
                    self._update_display()
                    self.last_display_update = current_time
                    
                # Small delay to prevent busy waiting
                time.sleep_ms(10)
                
            except Exception as e:
                print(f"Main loop error: {str(e)}")
                time.sleep_ms(1000)  # Delay to prevent rapid error messages

if __name__ == "__main__":
    sensor = CadenceSensor()
    if sensor.initialize():
        sensor.run()
    else:
        print("Failed to initialize cadence sensor!")