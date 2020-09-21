# -*- coding: utf-8 -*-
"""
Lights controller
"""

import machine
import config


class Light(object):

    def __init__(self, name, pin):
        self.name = name
        self._light = machine.Pin(pin, mode=machine.Pin.OUT, value=1)

    def on(self):
        if not self.is_on():
            print('Switching {} on.'.format(self.name))
            self._light.value(0)

    def off(self):
        if self.is_on():
            print('Switching {} off.'.format(self.name))
            self._light.value(1)

    def toggle(self):
        self._light.value(not self._light.value())
        print('Toggling {} to {}'.format(self.name, 'on' if self.is_on() else 'off'))

    def is_on(self):
        return not self._light.value()

    def print_status(self):
        print('{} is {}'.format(self.name, 'on' if self.is_on() else 'off'))


MAIN_LIGHT = Light('MAIN_LIGHT', config.PIN_L_MAIN)
BASKING_LIGHT = Light('BASKING_LIGHT', config.PIN_L_BASKING)
NIGHT_LIGHT = Light('NIGHT_LIGHT', config.PIN_L_NIGHT)
