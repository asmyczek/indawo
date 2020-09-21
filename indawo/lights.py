import machine
import config


class Light(object):

    def __init__(self, pin):
        self._light = machine.Pin(pin, mode=machine.Pin.OUT, value=1)

    def on(self):
        if not self.is_on():
            self._light.value(0)

    def off(self):
        if self.is_on():
            self._light.value(1)

    def toggle(self):
        self._light.value(not self._light.value())

    def is_on(self):
        return not self._light.value()


MAIN_LIGHT = Light(config.PIN_L_MAIN)
BASKING_LIGHT = Light(config.PIN_L_BASKING)
NIGHT_LIGHT = Light(config.PIN_L_NIGHT)
