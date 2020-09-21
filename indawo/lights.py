# -*- coding: utf-8 -*-
"""
Lights controller
"""

import machine
import config
import indawo.mqtt as mqtt


class Light(object):

    def __init__(self, name, pin):
        self.name = name
        self._light = machine.Pin(pin, mode=machine.Pin.OUT, value=1)

    def on(self):
        if not self.is_on():
            print('Switching {} on.'.format(self.name))
            self._light.value(0)
            mqtt.CLIENT.publish_light(self)

    def off(self):
        if self.is_on():
            print('Switching {} off.'.format(self.name))
            self._light.value(1)
            mqtt.CLIENT.publish_light(self)

    def toggle(self):
        self._light.value(not self._light.value())
        print('Toggling {} to {}'.format(self.name, 'on' if self.is_on() else 'off'))
        mqtt.CLIENT.publish_light(self)

    def is_on(self):
        return not self._light.value()

    def print_status(self):
        print('{} is {}'.format(self.name, 'on' if self.is_on() else 'off'))


MAIN_LIGHT = Light('MAIN', config.PIN_L_MAIN)
BASKING_LIGHT = Light('BASKING', config.PIN_L_BASKING)
NIGHT_LIGHT = Light('NIGHT', config.PIN_L_NIGHT)

LIGHTS = {
    'MAIN': MAIN_LIGHT,
    'BASKING': BASKING_LIGHT,
    'NIGHT': NIGHT_LIGHT
}

mqtt.CLIENT.set_lights_callback(lambda name: LIGHTS.get(name.upper(), None))
