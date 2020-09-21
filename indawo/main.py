# -*- coding: utf-8 -*-
"""
Main terrarium controller
"""

import indawo.environment as environment
import indawo.buttons as buttons
import indawo.lights as lights
import indawo.mqtt as mqtt
import uasyncio
import machine
import utime
import config
import time


MANUAL_CONTROL = False


async def controller():
    while True:
        if not MANUAL_CONTROL:
            y, m, d, h, m, s, ms, tz = utime.localtime()
            is_day = config.DAY_HOURS[0] <= h + 2 < config.DAY_HOURS[1]
            if environment.ENVIRONMENT.main_sensor_connected() and \
                    environment.ENVIRONMENT.temp_sensor_connected():
                if is_day:
                    lights.MAIN_LIGHT.on()
                    lights.NIGHT_LIGHT.off()
                    if environment.ENVIRONMENT.basking_temperature() < 32:
                        lights.BASKING_LIGHT.on()
                    if environment.ENVIRONMENT.basking_temperature() > 38:
                        lights.BASKING_LIGHT.off()
                else:
                    lights.MAIN_LIGHT.off()
                    lights.BASKING_LIGHT.off()
                    if environment.ENVIRONMENT.main_temperature() < 20:
                        lights.NIGHT_LIGHT.on()
                    if environment.ENVIRONMENT.main_temperature() > 24:
                        lights.NIGHT_LIGHT.off()
            else:
                if is_day:
                    lights.MAIN_LIGHT.on()
                    lights.BASKING_LIGHT.off()
                    lights.NIGHT_LIGHT.off()
                else:
                    lights.MAIN_LIGHT.off()
                    lights.BASKING_LIGHT.off()
                    lights.NIGHT_LIGHT.off()

        await uasyncio.sleep(60)


CONTROL_LOCK = uasyncio.Lock()


async def switch_to_auto_mode():
    await uasyncio.sleep(config.MANUAL_CONTROL_OVERRIDE_TIME * 60)
    global MANUAL_CONTROL
    print('Switching to automated control mode.')
    mqtt.CLIENT.publish_status('AUTO_MODE')
    CONTROL_LOCK.acquire()
    MANUAL_CONTROL = False
    if CONTROL_LOCK.locked():
        CONTROL_LOCK.release()


def button_trigger_callback(button):
    global MANUAL_CONTROL
    CONTROL_LOCK.acquire()
    if not MANUAL_CONTROL:
        print('Switching to manual control mode.')
        mqtt.CLIENT.publish_status('MANUAL_MODE')
        MANUAL_CONTROL = True
        loop = uasyncio.get_event_loop()
        loop.create_task(switch_to_auto_mode())
    if CONTROL_LOCK.locked():
        CONTROL_LOCK.release()


def start_service():
    print('Starting Indawo service.')
    print('Time: {}'.format(machine.RTC().datetime()))
    lights.MAIN_LIGHT.print_status()
    lights.BASKING_LIGHT.print_status()
    lights.NIGHT_LIGHT.print_status()
    mqtt.CLIENT.publish_status('STARTED')

    loop = uasyncio.get_event_loop()
    loop.create_task(environment.check_environment())
    time.sleep(3)
    loop.create_task(controller())
    loop.create_task(buttons.process_buttons(button_trigger_callback))
    try:
        loop.run_forever()
    except Exception as e:
        mqtt.CLIENT.publish_status('INTERRUPTED')
        mqtt.CLIENT.publish_error(e)
        print(e)
    print('Stopped Indawo service.')
    mqtt.CLIENT.publish_status('STOPPED')

