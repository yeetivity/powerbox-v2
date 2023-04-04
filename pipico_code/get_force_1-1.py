from machine import Pin
from hx711 import *
from utime import sleep_us
import struct, sys

led = Pin(25, Pin.OUT)

# 1. Initialise the hx711 with pin 14 as clock and 15 as data pin
hx = hx711(Pin(14), Pin(15))

# 2. Power up
hx.set_power(hx711.power.pwr_up)

# 3. Set gain and save it
hx.set_gain(hx711.gain.gain_64)
hx.set_power(hx711.power.pwr_down)
hx711.wait_power_down()
hx.set_power(hx711.power.pwr_up)

# 4. Wait for readings to settle
hx711.wait_settle(hx711.rate.rate_80)

def pack_message(force):
    msg = struct.pack("f", force)
    return msg

while True:
    sys.stdout.buffer.write(pack_message(hx.get_value()))
    led.toggle()
    sleep_us(12500)
