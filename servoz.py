import asyncio
import logging

log = logging.getLogger('servo_controller')

async def servo_controller(global_state):

    while True:
        log.debug("I'm a MOVING SERVO blinking - {}"
                  .format(global_state.head_servo_stage))
        sleepy_time = 0.5
        await asyncio.sleep(sleepy_time)
