from machine import Pin
from hx711 import *
from time import sleep_us
import struct
import sys

led = Pin(25, Pin.OUT)

t = 0

def pack_message(force):
    global t
    msg = struct.pack("f", force)
    #t = t + 1/10
    return msg

# 1. initalise the hx711(clk, data)
led.value(0)

with hx711(Pin(14), Pin(15)) as hx1:
    hx1.set_power(hx711.power.pwr_up)
    hx1.set_gain(hx711.gain.gain_64)
    hx1.wait_settle(hx711.rate.rate_80)
    while(True):
        print(hx1.get_value())
        #sys.stdout.buffer.write(pack_message(hx1.get_value()))
        sleep_us(12500)
        led.toggle()                    

# 6. stop communication with HX711
# hx.close()

