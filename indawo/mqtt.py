# -*- coding: utf-8 -*-
"""
MQTT client and APIs
"""

from umqtt.robust import MQTTClient
from ujson import loads, dumps
import config


class Client(object):

    def __init__(self):
        self._client = self._create_client()

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

    def on_message(self, topic, msg):
        print('{} - {}'.format(topic, msg))

    def publish_environment(self, stats):
        if self._client:
            self._client.publish(topic='terrarium/environment/stats', msg=dumps(stats))

    def publish_light(self, light):
        if self._client:
            self._client.publish(topic='terrarium/light/{}/status'.format(light.name), msg=light.is_on())

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

