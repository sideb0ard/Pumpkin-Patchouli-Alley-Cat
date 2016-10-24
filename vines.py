import RPi.GPIO as GPIO
import asyncio
import time
import logging

log = logging.getLogger('vines')

async def vines(global_state):
    pwm_pin = 4 

    print("vines")
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pwm_pin, GPIO.OUT)
    p = GPIO.PWM(pwm_pin, 50)

    sleepy_time = .5 

    p.start(0)

    while True:
        # song is 2:45. SHAKE until 2:40 then STILL for remainder
        if global_state.vines_stage == 'STILL':
            p.ChangeDutyCycle(0)
            await asyncio.sleep(sleepy_time)
        elif global_state.vines_stage == 'SHAKE':
            # opposite direction is p.ChangeDutyCycle(12)
            p.ChangeDutyCycle(3)
            await asyncio.sleep(sleepy_time)
