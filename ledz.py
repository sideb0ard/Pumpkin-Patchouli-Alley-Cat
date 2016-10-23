import asyncio
import logging
import random

import RPi.GPIO as GPIO

log = logging.getLogger('led_controller')

CUR_STAGE = ''
COUNTER = 0
LEN_PATTERN = 10
PERCENT_OF_PATTERN = 0
sleepy_time = 0.05


def update_counters_and_stage(global_state):

    global CUR_STAGE
    global COUNTER
    global LEN_PATTERN
    global PERCENT_OF_PATTERN
    global sleepy_time

    if CUR_STAGE != global_state.led_stage:
        if global_state.led_stage == 'RAND':
            COUNTER = 0
        elif global_state.led_stage == 'SYNC':
            COUNTER = LEN_PATTERN
        print("Changing STATE to {}".format(global_state.led_stage))
        CUR_STAGE = global_state.led_stage

    PERCENT_OF_PATTERN = COUNTER / LEN_PATTERN
    sleepy_time = 0.05  # randy

    if global_state.led_stage is 'RAND':
        COUNTER += sleepy_time
        if COUNTER > LEN_PATTERN:
            COUNTER = LEN_PATTERN
    elif global_state.led_stage == 'SYNC':
        COUNTER -= sleepy_time
        if COUNTER < 0:
            COUNTER = 0


def brightness():
   return random.randint(5, 100)


def flicker():
   return random.random() / 25


def new_rand_list():
    rands = []
    for x in range(52):
        rands.append(random.randint(0, 100))
    return rands


async def led_controller(global_state, pin):

    global CUR_STAGE
    global COUNTER
    global LEN_PATTERN
    global PERCENT_OF_PATTERN
    global sleepy_time

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(pin, GPIO.OUT)
    p = GPIO.PWM(pin, 100)
    p.start(0)

    dcz = []
    for x in range(0, 101, 4):
        dcz.append(x)
    for x in range(100, -1, 44):
        dcz.append(x)

    while True:

        randys = new_rand_list()

        for (i, dc) in enumerate(dcz):
            update_counters_and_stage(global_state)
            if CUR_STAGE == 'STEADY':
                p.ChangeDutyCycle(dc)
                await asyncio.sleep(sleepy_time)
            elif CUR_STAGE == 'RAND':
                p.ChangeDutyCycle(randys[i])
                await asyncio.sleep(sleepy_time)
            elif CUR_STAGE == 'SYNC':
                out = (PERCENT_OF_PATTERN * randys[i]) + \
                    ((1 - PERCENT_OF_PATTERN) * dc)
                p.ChangeDutyCycle(out)
                await asyncio.sleep(sleepy_time)

