"""
This is an optimized class to readout the status of two pins with encoder signals
No absolute angle is computed, just a signal per tick

The unoptimized class can be found in rotary2.py
"""

from machine import Pin
from micropython import schedule

class Rotary:

    ROT_CW = -1
    ROT_CCW = 1

    def __init__(self,dt1,dt2):
        self.dt1_pin = Pin(dt1, Pin.IN, Pin.PULL_DOWN)
        self.dt2_pin = Pin(dt2, Pin.IN, Pin.PULL_DOWN)
        self.last_status = (self.dt1_pin.value() << 1) | self.dt2_pin.value()
        self.dt1_pin.irq(handler=self.rotary_change, trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING )
        self.dt2_pin.irq(handler=self.rotary_change, trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING )
        self.handlers = []

    def rotary_change(self, pin):
        new_status = (self.dt1_pin.value() << 1) | self.dt2_pin.value()
        if new_status == self.last_status:
            return
        transition = (self.last_status << 2) | new_status
        if transition == 0b1110:
            schedule(self.call_handlers, Rotary.ROT_CW)
        elif transition == 0b1101:
            schedule(self.call_handlers, Rotary.ROT_CCW)
        self.last_status = new_status

    def add_handler(self, handler):
        #see if this can have only one handler to improve code speed
        self.handlers.append(handler)

    def call_handlers(self, type):
        for handler in self.handlers:
            handler(type)


