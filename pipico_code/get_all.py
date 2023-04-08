from rotary_optimized import Rotary
from utime import sleep_ms
from machine import Pin, Timer
from hx711 import hx711
import struct, gc, sys, _thread

#######################################################
##   SETUP
#######################################################

# Initialize on-board LED
led = Pin(25, Pin.OUT)

# Initialize variables
force1, force2, velocity, lines_moved, sample_nr = 0.0, 0.0, 0.0, 0, 0

# Initialize constants
FREQ_S = 50
DOWNSAMPLE = 5  # Ratio to downsample velocity with

# Create buffer for message
msg_buf = bytearray(struct.calcsize("fff"))

# Initialize rotary class with signal 1 and signal 2 pin
rotary = Rotary(2, 3)

# Initialize HX711 objects
hx1 = hx711(Pin(14), Pin(15), 0)
hx2 = hx711(Pin(16), Pin(17), 4)

# 2. power up
hx1.set_power(hx711.power.pwr_up)
hx2.set_power(hx711.power.pwr_up)

# 3. [OPTIONAL] set gain and save it to the hx711
# chip by powering down then back up
hx1.set_gain(hx711.gain.gain_64)
hx1.set_power(hx711.power.pwr_down)
hx711.wait_power_down()
hx1.set_power(hx711.power.pwr_up)

hx2.set_gain(hx711.gain.gain_64)
hx2.set_power(hx711.power.pwr_down)
hx711.wait_power_down()
hx2.set_power(hx711.power.pwr_up)

# 4. wait for readings to settle
hx711.wait_settle(hx711.rate.rate_80)

############################
# HELPER METHODS
############################

def force_thread():
    global force1
    global force2

    while True:
        force1 = hx1.get_value()
        force2 = hx2.get_value()
        sleep_ms(20)

def rotary_changed(change):
    global lines_moved
    lines_moved += change

def pack_message(velocity, force_1, force_2):
    msg = struct.pack("fff", velocity, force_1, force_2)
    return msg
    
def run(timer):
    led.toggle()
    global lines_moved
    global sample_nr
    global velocity

    if sample_nr % DOWNSAMPLE == 0:
        # Transform lines moved to velocity
        velocity = lines_moved * 0.0031415926535897933 * 10
        # Reset line counter (todo: maybe mutex flag (last resort))
        lines_moved = 0
        gc.collect()
    
    sample_nr += 1
    pack_message(velocity, force1, force2)
    
    print(gc.mem_free())

###########################
# MAIN
###########################

def main():
    """
    Some comment
    """
    rotary.add_handler(rotary_changed)

    _thread.start_new_thread(force_thread, ())

    timer = Timer()
    timer.init(freq=FREQ_S, mode=Timer.PERIODIC, callback=run)
    
main()



