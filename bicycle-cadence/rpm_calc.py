# rpm_calc.py
import time
import config

class RPMCalculator:
    def __init__(self):
        self.total_triggers = 0
        self.session_start_time = time.ticks_ms()
        
    def add_trigger(self):
        """Record a new trigger event"""
        self.total_triggers += 1
        
    def get_session_time(self):
        """Return current session time in minutes and seconds"""
        session_duration = time.ticks_diff(time.ticks_ms(), self.session_start_time)
        total_seconds = session_duration // 1000
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return minutes, seconds
        
    def reset(self):
        """Reset counter and session time"""
        self.total_triggers = 0
        self.session_start_time = time.ticks_ms()
        
    def get_stats(self):
        """Return dictionary with current statistics"""
        minutes, seconds = self.get_session_time()
        return {
            "total_triggers": self.total_triggers,
            "session_time": f"{minutes:02d}:{seconds:02d}"
        }