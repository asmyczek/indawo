# -*- coding: utf-8 -*-
"""
Environment controller
"""

import time
import dht
import config
import machine
import onewire
import ds18x20
import uasyncio
import indawo.mqtt as mqtt


PIN_S_MAIN = machine.Pin(config.PIN_S_MAIN)
PIN_S_TEMP = machine.Pin(config.PIN_S_TEMP)

S_TEMP_BASKING = bytearray(config.S_TEMP_BASKING)
S_TEMP_BASE = bytearray(config.S_TEMP_BASE)


class Environment(object):

    def __init__(self):
        self._s_main = None
        self._s_temp = None
        self._s_main_connected = False
        self._s_temp_connected = False
        self._state = {}
        self._s_main = dht.DHT22(PIN_S_MAIN)
        self._s_temp = ds18x20.DS18X20(onewire.OneWire(PIN_S_TEMP))

    def measure(self):
        try:
            self._s_main_connected = True
            self._s_main.measure()
        except OSError:
            self._s_main_connected = False
            print('Main sensor not connected!')
            mqtt.CLIENT.publish_error('Main sensor not connected.')

        try:
            self._s_temp_connected = True
            self._s_temp.convert_temp()
        except onewire.OneWireError:
            self._s_temp_connected = False
            print('Temp sensors not connected!')
            mqtt.CLIENT.publish_error('Temp sensor not connected.')

        time.sleep(1)

        if self._s_main_connected:
            self._state['temperature_main'] = self._s_main.temperature()
            self._state['humidity'] = self._s_main.humidity()
        else:
            self._state['temperature_main'] = 0.0
            self._state['humidity'] = 0.0

        if self._s_temp_connected:
            self._state['temperature_base'] = self._s_temp.read_temp(S_TEMP_BASE)
            self._state['temperature_basking'] = self._s_temp.read_temp(S_TEMP_BASE)
        else:
            self._state['temperature_base'] = 0.0
            self._state['temperature_basking'] = 0.0

        mqtt.CLIENT.publish_environment(self._s_main_connected and self._s_temp_connected, self._state)

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

    def temp_sensor_connected(self):
        return self._s_temp_connected

    def main_sensor_connected(self):
        return self._s_main_connected


ENVIRONMENT = Environment()


async def check_environment():
    while True:
        ENVIRONMENT.measure()
        await uasyncio.sleep(60)

