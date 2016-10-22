import asyncio
import logging
import random

MAX_DELAY = 1  # seconds

log = logging.getLogger('led_controller')

async def led_controller(global_state):

    base_sleepy_time = 0.018  # STEADY state

    LEN_TIMER = 10  # seconds
    CUR_TIMER = 10  # seconds

    while True:
        if global_state.led_stage == 'RAND':
            sleepy_time = base_sleepy_time + \
                (CUR_TIMER / LEN_TIMER * MAX_DELAY * random.random())

            CUR_TIMER -= sleepy_time
            if CUR_TIMER < 0:
                CUR_TIMER = 0
        else:
            CUR_TIMER = 10
            sleepy_time = base_sleepy_time

        log.debug("I'm a wee LED light blinking - blinking {} for {}"
                  .format(global_state.led_stage, sleepy_time))

        await asyncio.sleep(sleepy_time)
