from rotary_optimized import Rotary
from utime import sleep_us
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
FREQ_S = 80
DOWNSAMPLE = 8  # Ratio to downsample velocity with


#######################################################
##   COMPUTE VARIABLE THINGIES
#######################################################
TIMER_INTERVAL_US = 1000000 / FREQ_S


# Create buffer for message
# msg_buf = bytearray(struct.calcsize("fff"))

# Initialize rotary class with signal 1 and signal 2 pin
rotary = Rotary(2, 3)

# Initialize HX711 objects
hx1 = hx711(Pin(14), Pin(15), 4)
hx2 = hx711(Pin(16), Pin(17), 5)

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
        sleep_us(12500)

def rotary_changed(change):
    global lines_moved
    lines_moved += change

def pack_message(velocity, force_1, force_2):
    msg = struct.pack("fff", velocity, force_1, force_2)
    return msg
    
def run():
    led.toggle()
    global lines_moved
    global sample_nr
    global velocity
    
#     velocity = lines_moved * 0.0031415926535897933 * 10
#     lines_moved = 0
#     sys.stdout.buffer.write(pack_message(velocity, force1, force2))

    if sample_nr % DOWNSAMPLE == 0:
        # Transform lines moved to velocity
        velocity = lines_moved * 0.0031415926535897933 * 10
        lines_moved = 0
        
    
    sample_nr += 1
    sys.stdout.buffer.write(pack_message(velocity, force1, force2))
    print(gc.mem_free())
#     gc.collect()
###########################
# MAIN
###########################

def main():
    """
    Some comment
    """
    rotary.add_handler(rotary_changed)

    _thread.start_new_thread(force_thread, ())

    start_time = utime.ticks_us()
    last_interval_time = start_time

    while True:
        current_time = utime.ticks_us()

        if utime.ticks_diff(current_time, last_interval_time) >= TIMER_INTERVAL_US:
            run()
            last_interval_time = current_time
    
main()



