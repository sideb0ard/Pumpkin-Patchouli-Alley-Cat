import RPi.GPIO as GPIO
import asyncio
import time
import logging

log = logging.getLogger('servo_controller')

async def servo_controller(global_state):

    print("SERVO CCALLED")
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.OUT)
    p = GPIO.PWM(17, 50)

    sleepy_time = 2

    p.start(0)

    while True:
        
        # for x in range( 30 ):
        # log.debug("I'm a MOVING SERVO blinking - {}".format(x))
        # p.ChangeDutyCycle(0)
        # await asyncio.sleep(sleepy_time)

        p.ChangeDutyCycle(3)
        await asyncio.sleep(sleepy_time)

        p.ChangeDutyCycle(0)
        await asyncio.sleep(sleepy_time)

        p.ChangeDutyCycle(12)
        await asyncio.sleep(sleepy_time)

        p.ChangeDutyCycle(0)
        await asyncio.sleep(sleepy_time)
