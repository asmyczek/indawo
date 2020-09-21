# -*- coding: utf-8 -*-
"""
MQTT client and APIs
"""

from umqtt.robust import MQTTClient
from ujson import dumps
import config


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
            client.connect()
            client.subscribe(topic='terrarium/#')
            return client
        except Exception as e:
            print(e)
            return None

    def set_lights_callback(self, callback):
        self._lights_callback = callback

    def on_message(self, topic, msg):
        print('{} - {}'.format(topic, msg))
        path = topic.split('/')
        if path[1] == 'light' and self._lights_callback:
            light = self._lights_callback(path[2])
            if light:
                if msg == 'on':
                    light.on()
                elif msg == 'off':
                    light.off()
                else:
                    emsg = 'Invalid light state {}. Expecting on or off.'.format(msg)
                    print(emsg)
                    self.publish_error(emsg)
            else:
                emsg = 'Invalid light name {}.'.format(path[2])
                print(emsg)
                self.publish_error(emsg)

    def publish_environment(self, stats):
        if self._client:
            self._client.publish(topic='terrarium/environment/stats', msg=dumps(stats))

    def publish_light(self, light):
        if self._client:
            self._client.publish(topic='terrarium/light/{}/status'.format(light.name),
                                 msg='on' if light.is_on() else 'off')

    def publish_button_trigger(self, button):
        if self._client:
            self._client.publish(topic='terrarium/button/{}/trigger'.format(button.name))

    def publish_status(self, status):
        if self._client:
            self._client.publish(topic='terrarium/status', msg=status)

    def publish_error(self, error):
        if self._client:
            self._client.publish(topic='terrarium/error', msg=error)


CLIENT = Client()

