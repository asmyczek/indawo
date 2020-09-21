# -*- coding: utf-8 -*-
"""
REPL tools

Howto:
- Login to REPL or WEB_REPL
- Type CTRL-C to stop main loop
- import tools
"""

import machine
from indawo.lights import MAIN_LIGHT, BASKING_LIGHT, NIGHT_LIGHT
from indawo.environment import ENVIRONMENT


def environment_stats():
    ENVIRONMENT.measure()
    for k, v in ENVIRONMENT.stats().items():
        print(k + ': ' + str(v))


def lights_status():
    MAIN_LIGHT.print_status()
    BASKING_LIGHT.print_status()
    NIGHT_LIGHT.print_status()


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
