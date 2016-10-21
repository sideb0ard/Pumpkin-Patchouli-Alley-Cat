import asyncio
import logging
import random

log = logging.getLogger('led_controller')

async def led_controller(global_state):
    while True:
        log.debug("I'm a wee LED light blinking - blinking {} randomly"
                  .format(global_state.led_stage))
        if global_state.led_stage == 'RAND':
            sleepy_time = random.random() * 2
        else:
            sleepy_time = 2
        await asyncio.sleep(sleepy_time)
