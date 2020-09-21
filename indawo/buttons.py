# -*- coding: utf-8 -*-
"""
Button controller
"""

import machine
import uasyncio
import indawo.lights as lights

PIN_BUTTONS = adc = machine.ADC(0)


class Button(object):

    def __init__(self, name, from_level, to_level, trigger):
        self.name = name
        self._from = from_level
        self._to = to_level
        self._trigger = trigger
        self._state = False

    def try_on(self, analog_level):
        if self._from <= analog_level <= self._to:
            self._state = True
            return True
        else:
            return False

    def trigger(self):
        if self._state:
            print('Button {} triggered.'.format(self.name))
            self._trigger()
            self._state = False
            return True
        else:
            return False


BUTTONS = [
    Button('MAIN_LIGHT', 1, 10, lights.MAIN_LIGHT.toggle),
    Button('BASKING_LIGHT', 535, 545, lights.BASKING_LIGHT.toggle),
    Button('NIGHT_LIGHT', 710, 720, lights.NIGHT_LIGHT.toggle)
]


async def process_buttons(trigger_callback):
    last_analog_level = 1024
    while True:
        analog_level = PIN_BUTTONS.read()
        if analog_level != last_analog_level:
            for button in BUTTONS:
                if analog_level < 1024:
                    button.try_on(analog_level)
                else:
                    if button.trigger():
                        trigger_callback(button)

        last_analog_level = analog_level
        await uasyncio.sleep_ms(100)
