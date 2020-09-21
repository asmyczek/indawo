# Set of monitoring commands and actions for repl
import machine
from indawo.lights import MAIN_LIGHT, BASKING_LIGHT, NIGHT_LIGHT
from indawo.environment import ENVIRONMENT


def environment_stats():
    ENVIRONMENT.measure()
    for k, v in ENVIRONMENT.stats().items():
        print(k + ': ' + str(v))


def lights_status():
    print('Main light: {}'.format('on' if MAIN_LIGHT.is_on() else 'off'))
    print('Basking light: {}'.format('on' if BASKING_LIGHT.is_on() else 'off'))
    print('Night light: {}'.format('on' if NIGHT_LIGHT.is_on() else 'off'))


def reboot():
    machine.reset()


def help():
    print('''
    Available tool functions:
    - environment_stats() - print current temperature and humidity
    - {MAIN, BASKING, NIGHT}_LIGHT
      .on()      - get current temperature and humidity
      .off()     - get current temperature and humidity
      .is_on()   - get current temperature and humidity
      for example MAIN_LIGHT.on()
    - lights_status() - print on/off status for all lights 
    ''')
