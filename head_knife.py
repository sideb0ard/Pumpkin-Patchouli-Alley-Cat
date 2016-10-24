import RPi.GPIO as GPIO
import asyncio
import time
import logging

log = logging.getLogger('head_knife')

async def head_knife(global_state):
    # RPi 3b worked with 17
    pwm_pin = 22 

    print("Face... off...")
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pwm_pin, GPIO.OUT)
    p = GPIO.PWM(pwm_pin, 50)

    sleepy_time = .5 

    p.start(0)

    while True:
        # song is 2:45. slice until 2:00 then stab for remainder
        if global_state.carve_servo_stage == 'ROUND':
            # opposite direction is p.ChangeDutyCycle(12)
            p.ChangeDutyCycle(3)
            await asyncio.sleep(sleepy_time)
        elif global_state.carve_servo_stage == 'STAB':
            p.ChangeDutyCycle(0)
            await asyncio.sleep(sleepy_time)
