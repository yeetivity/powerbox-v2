from rotary_optimized import Rotary
from utime import ticks_us, ticks_diff, sleep_ms
from machine import Pin, UART, Timer
from hx711 import *
import struct
import sys
import _thread

force1 = 0.0
force2 = 0.0

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
    hx1.set_gain(hx711.gain.gain_128)
    hx1.set_power(hx711.power.pwr_down)
    hx711.wait_power_down()
    hx1.set_power(hx711.power.pwr_up)

    hx2.set_gain(hx711.gain.gain_128)
    hx2.set_power(hx711.power.pwr_down)
    hx711.wait_power_down()
    hx2.set_power(hx711.power.pwr_up)

    # 4. wait for readings to settle
    hx711.wait_settle(hx711.rate.rate_10)

    while(True):
        force1 = hx1.get_value()
        force2 = hx2.get_value()

        # print(f'{force1}   {force2}')



#######################################################
##   SETUP
#######################################################

# Initialize on-board LED
led = Pin(25, Pin.OUT)

# Initialize variables #todo: change initialization of forces
last_tick, av, force1, force2, lines_moved = 0.0, 0.0, 0.0, 0.0, 0

# Initialize rotary class with signal 1 and signal 2 pin
rotary = Rotary(2, 3)



# HELPER METHODS
############################


def rotary_changed2(change):
    global last_tick
    global av
    
    #Todo: change methodology to counting lines

    #determine current time
    tick = ticks_us()
    #determine time difference
    dt = ticks_diff(tick, last_tick)
    
    if change == Rotary.ROT_CW:
        #counterclockwise rotation
        direction = -1
    elif change == Rotary.ROT_CCW:
        #clockwise rotation
        direction = 1
    #angular velocity
    av = direction * 1.44 / dt
    # print(av)
    #update last time
    last_tick = tick
        

def rotary_changed(change):
    global lines_moved

    lines_moved += change


def pack_message(speed, force_1, force_2):
    msg = struct.pack("fff", speed, force_1, force_2)
    return msg
    

def run(timer):    
    led.toggle()
    global av
    global lines_moved

    # Compute speed [degrees/second]
    av = (lines_moved * 1.44) / (1/10)
    # Reset line counter
    lines_moved = 0

    sys.stdout.buffer.write(pack_message(av, force1, force2))
    # print(f'{av}  {force1}  {force2}')



# MAIN
###########################

def main():
    """
    Some comment
    """
    rotary.add_handler(rotary_changed)

    # Timer for getting the data on 60 Hz
    timer = Timer()
    timer.init(freq=10, mode=Timer.PERIODIC, callback=run)

    #uncomment if you want to use GPIO uart
    #uart = UART(0, baudrate=115200, tx=Pin(16), rx=Pin(17))
    #uart.init(bits=8, parity=None, stop=2)
    _thread.start_new_thread(force_thread(), ())



main()

