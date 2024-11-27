# config.py
from micropython import const

# Pin Configurations
PIN_REED_SWITCH = const(15)
PIN_BUTTON = const(16)
PIN_SDA = const(0)
PIN_SCL = const(1)
PIN_LED = const(13)  # Added LED pin configuration

# Timing Constants (in milliseconds)
DEBOUNCE_TIME_MS = const(100)
REED_SWITCH_DEAD_TIME = const(200)
LONG_PRESS_TIME_MS = const(1000)
SHORT_PRESS_WINDOW_MS = const(500)
DISPLAY_REFRESH_MS = const(100)
LED_FLASH_DURATION_MS = const(50)  # Added LED flash duration

# Sleep Mode
DEEP_SLEEP_WAKE_PIN = PIN_BUTTON
SHORT_PRESS_COUNT_FOR_SLEEP = const(5)

# Display Settings
OLED_WIDTH = const(128)
OLED_HEIGHT = const(64)
OLED_ADDR = const(0x3C)

# Error Codes
ERR_HARDWARE_INIT = const(1)
ERR_SENSOR_READ = const(2)
ERR_DISPLAY = const(3)