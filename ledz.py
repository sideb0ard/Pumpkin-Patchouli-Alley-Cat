import asyncio
import logging
import random

import RPi.GPIO as GPIO

log = logging.getLogger('led_controller')


async def led_controller(global_state, pin):

    CUR_STAGE = ''
    COUNTER = 0.1
    LEN_PATTERN = 10

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    p = GPIO.PWM(pin, 100)

    p.start(0)
    sleepy_time = 0.05

    while True:

        #  print("COunter {}".format(COUNTER))
        if CUR_STAGE != global_state.led_stage:
            print("Changing STATE to {}".format(global_state.led_stage))
            if global_state.led_stage == 'RAND':
                COUNTER = 0.1
            elif global_state.led_stage == 'SYNC':
                COUNTER = LEN_PATTERN
            print("Setting COUNTER to {}".format(COUNTER))
            CUR_STAGE = global_state.led_stage

        randy_int = int(0.05 * (COUNTER / LEN_PATTERN) * 10000)
        randy = random.randrange(0, randy_int) / 10000
        print("RANDY is {}".format(randy))
        sleepy_time = 0.05 - randy
        print("SLEEPTIME is {}".format(sleepy_time))

        if global_state.led_stage is 'RAND':
            COUNTER += sleepy_time
            if COUNTER > LEN_PATTERN:
                COUNTER = LEN_PATTERN
        else:  # SYNC
            COUNTER -= sleepy_time
            if COUNTER < 0:
                COUNTER = 0

        for dc in range(0, 101, 4): # Increase duty cycle: 0~100
                if CUR_STAGE == 'RAND':
                    dc = (dc + (random.random() * COUNTER/LEN_PATTERN)) % 100
                    print("RANDOM DC is {}".format(dc))
                p.ChangeDutyCycle(dc) # Change duty cycle
                await asyncio.sleep(sleepy_time)

        for dc in range(100, -1, -4): # Decrease duty cycle: 100~0
                if CUR_STAGE == 'RAND':
                    dc = (dc + (random.random() * COUNTER/LEN_PATTERN)) % 100
                    print("RANDOM DC is {}".format(dc))
                p.ChangeDutyCycle(dc)
                await asyncio.sleep(sleepy_time)

