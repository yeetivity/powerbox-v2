from rotary_irq_rp2 import RotaryIRQ
import utime, struct, sys
from machine import Pin, Timer
from hx711 import hx711

#######################################################
##   SETTINGS
#######################################################

led = Pin(25, Pin.OUT)  # On-board LED

DT_FL = 14  # Data pin, force sensor left
CLK_FL = 15  # Cock pin, force sensor left

DT_FR = 16  # Data pin, force sensor left
CLK_FR = 17  # Cock pin, force sensor left

S1_V = 3  # Signal one, rotary encoder
S2_V = 2  # Signal two, rotary encoder

FREQ_F = 80  # Frequency for force acquirement
FREQ_V = 10  # Frequency for velocity acquirement

nlines_old, sample_nr, velocity = 0, 0, 0.0  # Initializing variables

#----------------------
#  COMPUTING CONSTANTS
#----------------------
TIMER_INTERVAL_US = 1000000 / FREQ_F  # Time in microseconds for each sample
R_DOWNSAMPLE = FREQ_F/FREQ_V  # Ratio to downsample with


#######################################################
##   SETUP
#######################################################

rotary = RotaryIRQ(pin_num_clk=S1_V,
                   pin_num_dt=S2_V,
                   reverse=False,
                   range_mode=RotaryIRQ.RANGE_UNBOUNDED)

adc_left = hx711(Pin(DT_FL), Pin(CLK_FL), 0)
adc_right = hx711(Pin(DT_FR), Pin(CLK_FR), 4)

#######################################################
##   STARTUP
#######################################################

# Show start sequence leds
for i in range(3):
    led.toggle
    utime.sleep_us(500000)

# Power up adcs
adc_left.set_power(hx711.power.pwr_up)
adc_right.set_power(hx711.power.pwr_up)

# Set gains
def set_gain(adc):
    adc.set_gain(hx711.gain.gain_64)
    adc.set_power(hx711.power.pwr_down)
    hx711.wait_power_down()
    adc.set_power(hx711.power.pwr_up)

set_gain(adc=adc_left)
set_gain(adc=adc_right)

# Wait for readings to settle
hx711.wait_settle(hx711.rate.rate_80)

############################
# RUN METHODS
############################

def pack_message(velocity, force_1, force_2):
    return struct.pack("fff", velocity, force_1, force_2)
    
def run():
    global nlines_old
    global sample_nr
    global velocity

    led.toggle()

    if sample_nr % R_DOWNSAMPLE == 0:
        lines_moved = rotary.value()   # Get current reading
        displacement = lines_moved - nlines_old  # Compute displacement 
        nlines_old = lines_moved  # Update previous reading
        velocity = displacement * 0.031415926535897933

    force_left = adc_left.get_value()
    force_right = adc_right.get_value()
    sample_nr += 1
        
    sys.stdout.buffer.write(pack_message(velocity, force_left, force_right))

def main():
    start_time = utime.ticks_us()
    last_interval_time = start_time
    
    while True:
        current_time = utime.ticks_us()

        if utime.ticks_diff(current_time, last_interval_time) >= TIMER_INTERVAL_US:
            run()
            last_interval_time = current_time
    
main()
