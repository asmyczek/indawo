# -*- coding: utf-8 -*-
"""
MQTT client and APIs
"""

from umqtt.robust import MQTTClient
from ujson import dumps
import config
import uasyncio


class Client(object):

    def __init__(self):
        self._client = self._create_client()
        self._lights_callback = None

    def _create_client(self):
        try:
            client = MQTTClient('terrarium',
                                config.MQTT_HOST,
                                user=config.MQTT_USER,
                                password=config.MQTT_PASSWORD,
                                port=config.MQTT_PORT)
            client.set_callback(self.on_message)
            if not client.connect(clean_session=False):
                print("MQTT new session being set up.")
                client.subscribe('cmnd/terrarium/#', qos=1)
            return client
        except Exception as e:
            print(e)
            return None

    def check_msg(self):
        self._client.check_msg()

    def set_lights_callback(self, callback):
        self._lights_callback = callback

    def on_message(self, topic, message):
        print('{} - {}'.format(topic, message))
        path = topic.decode("utf-8").split('/')
        if path[2] == 'light' and self._lights_callback:
            light = self._lights_callback(path[3])
            msg = message.decode("utf-8")
            if light:
                if msg.upper() == 'ON':
                    light.on()
                elif msg.upper() == 'OFF':
                    light.off()
                elif msg is None or msg == '':
                    self.publish_light(light)
                else:
                    emsg = 'Invalid light state {}. Expecting on or off.'.format(msg)
                    print(emsg)
                    self.publish_error(emsg)
            else:
                emsg = 'Invalid light name {}.'.format(path[2])
                print(emsg)
                self.publish_error(emsg)

    def publish_environment(self, connected, stats):
        if self._client:
            message = {'connected': connected,
                       'stats': stats}
            self._client.publish(topic='stats/terrarium/environment/stats', msg=dumps(message))

    def publish_light(self, light):
        if self._client:
            self._client.publish(topic='stats/terrarium/light/{}/power'.format(light.name.lower()),
                                 msg='ON' if light.is_on() else 'OFF')

    def publish_button_trigger(self, button):
        if self._client:
            self._client.publish(topic='stats/terrarium/button/{}/trigger'.format(button.name.lower()))

    def publish_status(self, status):
        if self._client:
            self._client.publish(topic='stats/terrarium/status', msg=status)

    def publish_mode(self, mode):
        if self._client:
            self._client.publish(topic='stats/terrarium/mode', msg=mode)

    def publish_error(self, error):
        if self._client:
            self._client.publish(topic='info/terrarium/error', msg=error)


CLIENT = Client()


async def start_mqtt_client():
    while True:
        CLIENT.check_msg()
        await uasyncio.sleep(1)

    CLIENT.disconnect()

