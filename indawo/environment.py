import time
import dht
import config
import machine
import onewire
import ds18x20
import uasyncio


PIN_S_MAIN = machine.Pin(config.PIN_S_MAIN)
PIN_S_TEMP = machine.Pin(config.PIN_S_TEMP)

S_TEMP_BASKING = bytearray(config.S_TEMP_BASKING)
S_TEMP_BASE = bytearray(config.S_TEMP_BASE)


class Environment(object):

    def __init__(self):
        self._s_main = None
        self._s_temp = None
        self._state = {}
        self._init_sensors()

    def _init_sensors(self):
        self._s_main = dht.DHT22(PIN_S_MAIN)
        self._s_temp = ds18x20.DS18X20(onewire.OneWire(PIN_S_TEMP))

    def measure(self):
        try:
            get_main_stats = True
            self._s_main.measure()
        except OSError:
            get_main_stats = False
            print('Main sensor not connected!')

        try:
            get_temp_stats = True
            self._s_temp.convert_temp()
        except onewire.OneWireError:
            get_temp_stats = False
            print('Temp sensors not connected!')

        time.sleep(1)

        if get_main_stats:
            self._state['temperature_main'] = self._s_main.temperature()
            self._state['humidity'] = self._s_main.humidity()
        else:
            self._state['temperature_main'] = 0.0
            self._state['humidity'] = 0.0

        if get_temp_stats:
            self._state['temperature_base'] = self._s_temp.read_temp(S_TEMP_BASE)
            self._state['temperature_basking'] = self._s_temp.read_temp(S_TEMP_BASE)
        else:
            self._state['temperature_base'] = 0.0
            self._state['temperature_basking'] = 0.0

    def main_temperature(self):
        return self._state['temperature_main']

    def basking_temperature(self):
        return self._state['temperature_basking']

    def base_temperature(self):
        return self._state['temperature_base']

    def humidity(self):
        return self._state['humidity']

    def stats(self):
        return self._state


ENVIRONMENT = Environment()


async def check_environment():
    while True:
        ENVIRONMENT.measure()
        await uasyncio.sleep(60)
