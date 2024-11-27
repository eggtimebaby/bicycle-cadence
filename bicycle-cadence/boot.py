import webrepl
import network
import time

def wifi_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect('MySpectrumWiFid0-2G', 'plainpoodle267')
    while not wlan.isconnected():
        time.sleep_ms(100)

wifi_connect()
webrepl.start()