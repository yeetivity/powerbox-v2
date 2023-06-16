from rotary_optimized import Rotary
from utime import ticks_us, ticks_diff
from machine import Pin, UART, Timer
from hx711 import *
import struct
import sys

#Initialize rotary class with signal 1 and signal 2 pin
rotary = Rotary(2, 3)
#todo: initialize adcs
#Initialize on-board LED
led = Pin(25, Pin.OUT)
#Initialize variables #todo: change initialization of forces
lines_moved = 0
FREQ_S = 10

def rotary_changed(change):
    global lines_moved
    
    lines_moved += change
    
def pack_message(lines, velocity):
    msg = struct.pack("ff", lines, velocity)
    return msg
    
def run(timer):
    global lines_moved
    global FREQ_S
    
    led.toggle()
    
    # Compute velocity
    velocity = lines_moved * 0.0031415926535897933 * FREQ_S
    sys.stdout.buffer.write(pack_message(lines_moved, velocity))
    # Reset line counter
    lines_moved = 0
    


rotary.add_handler(rotary_changed)

#timer for getting the data on 60 Hz
timer = Timer()
timer.init(freq=FREQ_S, mode=Timer.PERIODIC, callback=run)





    






