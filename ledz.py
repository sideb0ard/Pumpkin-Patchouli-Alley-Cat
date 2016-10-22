import asyncio
import logging
import random

log = logging.getLogger('led_controller')

async def led_controller(global_state, pin):

    base_sleepy_time = 0.018  # STEADY state

    LEN_PATTERN = 10  # seconds. Should match sleep time i timerrr
    MAX_DELAY = 1  # seconds
    STEADY_COUNTUP = 0
    SYNC_COUNTDOWN = LEN_PATTERN

    while True:

        sleepy_time = base_sleepy_time

        if global_state.led_stage == 'STEADY':
            SYNC_COUNTDOWN = LEN_PATTERN
            sleepy_time += + \
                (STEADY_COUNTUP / LEN_PATTERN * MAX_DELAY * random.random())
            STEADY_COUNTUP += sleepy_time
            if STEADY_COUNTUP > LEN_PATTERN:
                STEADY_COUNTUP = LEN_PATTERN

        elif global_state.led_stage == 'SYNC':
            STEADY_COUNTUP = 0  # reset countup
            sleepy_time += + \
                (SYNC_COUNTDOWN / LEN_PATTERN * MAX_DELAY * random.random())
            SYNC_COUNTDOWN -= sleepy_time
            if SYNC_COUNTDOWN < 0:
                SYNC_COUNTDOWN = 0

        log.debug("I'm LED light {} - blinking {} for {}"
                  .format(pin, global_state.led_stage, sleepy_time))

        await asyncio.sleep(sleepy_time)
