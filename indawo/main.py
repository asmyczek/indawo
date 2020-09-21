# http://www.ignorantofthings.com/2018/07/the-perfect-multi-button-input-resistor.html
# https://lastminuteengineers.com/esp8266-dht11-dht22-web-server-tutorial/


import indawo.environment as environment
import indawo.buttons as buttons
import indawo.lights as lights
import uasyncio
import machine
import utime
import config


MANUAL_CONTROL = False


async def controller():
    while True:
        if not MANUAL_CONTROL:
            y, m, d, w, h, m, s, ms = utime.localtime()
            is_day = config.DAY_HOURS[0] <= h + 2 < config.DAY_HOURS[1]
            if is_day:
                lights.MAIN_LIGHT.on()
                if environment.ENVIRONMENT.basking_temperature() < 32:
                    lights.BASKING_LIGHT.on()
                if environment.ENVIRONMENT.basking_temperature() > 38:
                    lights.BASKING_LIGHT.off()
            else:
                lights.MAIN_LIGHT.off()
                if environment.ENVIRONMENT.main_temperature() < 20:
                    lights.NIGHT_LIGHT.on()
                if environment.ENVIRONMENT.main_temperature() > 24:
                    lights.NIGHT_LIGHT.off()

        await uasyncio.sleep(60)


CONTROL_LOCK = uasyncio.Lock()


async def switch_to_auto_mode():
    await uasyncio.sleep(config.MANUAL_CONTROL_OVERRIDE_TIME * 60)
    global MANUAL_CONTROL
    print('Switching to automated control mode.')
    CONTROL_LOCK.acquire()
    MANUAL_CONTROL = False
    if CONTROL_LOCK.locked():
        CONTROL_LOCK.release()


def button_trigger_callback(button):
    global MANUAL_CONTROL
    CONTROL_LOCK.acquire()
    if not MANUAL_CONTROL:
        print('Switching to manual control mode.')
        MANUAL_CONTROL = True
        loop = uasyncio.get_event_loop()
        loop.create_task(switch_to_auto_mode())
    if CONTROL_LOCK.locked():
        CONTROL_LOCK.release()


def start_service():
    print('Starting Indawo service.')
    print('Time: {}'.format(machine.RTC().datetime()))
    loop = uasyncio.get_event_loop()
    loop.create_task(buttons.process_buttons(button_trigger_callback))
    loop.create_task(environment.check_environment())
    try:
        loop.run_forever()
    except Exception as e:
        print(e)
    print('Stopped Indawo service.')

