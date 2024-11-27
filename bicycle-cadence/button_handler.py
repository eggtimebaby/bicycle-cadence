# button_handler.py
import time
import config

class ButtonHandler:
    def __init__(self):
        self.last_press_time = 0
        self.press_start_time = 0
        self.short_press_count = 0
        self.last_short_press_time = 0
        self.is_pressed = False
        self.sleep_mode = False
        self.display_mode = 0  # 0 for raw count, 1 for RPM
        
    def handle_press(self, pin_value):
        """Handle button press events with debouncing"""
        current_time = time.ticks_ms()
        
        # Debounce check
        if time.ticks_diff(current_time, self.last_press_time) < config.DEBOUNCE_TIME_MS:
            return None
            
        self.last_press_time = current_time
        
        # Button pressed (remember, pull-up means 0 is pressed)
        if pin_value == 0 and not self.is_pressed:
            self.is_pressed = True
            self.press_start_time = current_time
            return "PRESS_START"
            
        # Button released
        elif pin_value == 1 and self.is_pressed:
            self.is_pressed = False
            press_duration = time.ticks_diff(current_time, self.press_start_time)
            
            # Long press detection
            if press_duration >= config.LONG_PRESS_TIME_MS:
                return "LONG_PRESS"
                
            # Short press handling
            else:
                self.short_press_count += 1
                
                # Reset short press counter if window expired
                if time.ticks_diff(current_time, self.last_short_press_time) > config.SHORT_PRESS_WINDOW_MS:
                    self.short_press_count = 1
                
                self.last_short_press_time = current_time
                
                # Check for sleep toggle condition
                if self.short_press_count >= config.SHORT_PRESS_COUNT_FOR_SLEEP:
                    self.short_press_count = 0
                    self.sleep_mode = not self.sleep_mode
                    return "TOGGLE_SLEEP"
                
                # Single short press toggles display mode
                return "SHORT_PRESS"
        
        return None
    
    def clear_press_count(self):
        """Reset short press counter"""
        self.short_press_count = 0
        
    def get_sleep_mode(self):
        """Return current sleep mode status"""
        return self.sleep_mode
    
    def toggle_display_mode(self):
        """Toggle between raw count and RPM display modes"""
        self.display_mode = 1 - self.display_mode
        return self.display_mode
    
    def get_display_mode(self):
        """Return current display mode"""
        return self.display_mode