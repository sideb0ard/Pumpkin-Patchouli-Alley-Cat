import RPi.GPIO as GPIO
import asyncio
import time
import logging

log = logging.getLogger('servo_controller')

async def servo_controller(global_state):

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(12, GPIO.OUT)
    p = GPIO.PWM(12, 50)
    p.start(7.5)

    while True:
        log.debug("I'm a MOVING SERVO blinking - {}"
                  .format(global_state.head_servo_stage))
        p.ChangeDutyCycle(7.5)  # turn towards 90 degree

        sleepy_time = 1
        await asyncio.sleep(sleepy_time)

        p.stop()
        GPIO.cleanup()
