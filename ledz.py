import asyncio
import logging
import random

import RPi.GPIO as GPIO

log = logging.getLogger('led_controller')

async def led_controller(global_state, pin):

    base_sleepy_time = 0.018  # STEADY state
    CUR_STAGE = ''

    LEN_PATTERN = 10  # seconds. Should match sleep time i timerrr
    MAX_DELAY = 3  # seconds
    COUNTER = 0

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    pwm = GPIO.PWM(pin, 100)


    while True:

        # reset COUNTER when stage changes
        if CUR_STAGE != global_state.led_stage:
            if global_state.led_stage == 'STEADY':
                COUNTER = 0
            elif global_state.led_stage == 'SYNC':
                COUNTER = LEN_PATTERN
            CUR_STAGE = global_state.led_stage

        sleepy_time = base_sleepy_time + \
            (COUNTER / LEN_PATTERN * MAX_DELAY * random.random())

        if global_state.led_stage == 'STEADY':
            COUNTER += sleepy_time
            if COUNTER > LEN_PATTERN:
                COUNTER = LEN_PATTERN

        elif global_state.led_stage == 'SYNC':
            COUNTER -= sleepy_time
            if COUNTER < 0:
                COUNTER = 0

        pwm.start(0)
        pwm.ChangeDutyCycle(random.randint(5, 100))

        log.debug("I'm LED light {} - blinking {} for {}"
                  .format(pin, global_state.led_stage, sleepy_time))

        await asyncio.sleep(sleepy_time)
