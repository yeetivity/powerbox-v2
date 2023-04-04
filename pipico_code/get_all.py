from rotary_optimized import Rotary
from utime import ticks_us, ticks_diff, sleep_us
from machine import Pin, UART, Timer
from hx711 import *
import struct
import sys
import _thread

#######################################################
##   SETUP
#######################################################

# Initialize on-board LED
led = Pin(25, Pin.OUT)

# Initialize variables
force1, force2, velocity, lines_moved, sample_nr = 0.0, 0.0, 0.0, 0, 0
FREQ_S = 80
DOWNSAMPLE = 8  # Ratio to downsample velocity with

# Initialize rotary class with signal 1 and signal 2 pin
rotary = Rotary(2, 3)

############################
# HELPER METHODS
############################

def force_thread():
    global force1
    global force2

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

    while(True):
        force1 = hx1.get_value()
        force2 = hx2.get_value()
        sleep_us(12500)

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

    if (sample_nr % DOWNSAMPLE) == 0:
        # Transform lines moved to velocity
        velocity = lines_moved * 0.0031415926535897933 * FREQ_S
        # Reset line counter
        lines_moved = 0
        # Reset sample counter to prevent big integer
        sample_nr = 1
    
    sample_nr += 1
    sys.stdout.buffer.write(pack_message(velocity, force1, force2))

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


