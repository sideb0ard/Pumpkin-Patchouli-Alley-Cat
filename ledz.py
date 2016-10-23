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
        elif global_state.led_stage == 'STEADY':
            COUNTER = LEN_PATTERN
        print("Changing STATE to {}".format(global_state.led_stage))
        CUR_STAGE = global_state.led_stage

    
    PERCENT_OF_PATTERN = COUNTER / LEN_PATTERN
    randy = 0.05 * PERCENT_OF_PATTERN * random.random()
    sleepy_time = 0.05 - randy

    if global_state.led_stage is 'RAND':
        COUNTER += sleepy_time
        if COUNTER > LEN_PATTERN:
            COUNTER = LEN_PATTERN
    else:  # SYNC
        COUNTER -= sleepy_time
        if COUNTER < 0:
            COUNTER = 0

    # print("COUNTER {}".format(COUNTER))

def brightness():
   return random.randint(5, 100)
def flicker():
   return random.random() / 25

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

    while True:

        if CUR_STAGE == 'STEADY':
            for dc in range(0, 101, 4): # Increase duty cycle: 0~100
                print("CURSTAGE {}".format(CUR_STAGE))
                update_counters_and_stage(global_state)
                # dc = (dc + (random.random() * PERCENT_OF_PATTERN)) % 100
                p.ChangeDutyCycle(dc) # Change duty cycle
                await asyncio.sleep(sleepy_time)

            for dc in range(100, -1, -4): # Decrease duty cycle: 100~0
                print("CURSTAGE {}".format(CUR_STAGE))
                update_counters_and_stage(global_state)
                # dc = (dc + (random.random() * COUNTER/LEN_PATTERN)) % 100
                p.ChangeDutyCycle(dc) # Change duty cycle
                await asyncio.sleep(sleepy_time)
        else:
            print("CURSTAGE {}".format(CUR_STAGE))
            update_counters_and_stage(global_state)
            p.ChangeDutyCycle(brightness())
            # Randomly pause on a brightness to simulate flickering
            await asyncio.sleep(flicker())
