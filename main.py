#!/usr/bin/env python
# needs python >= 3.5 for asyncio

import argparse
import asyncio
import functools
import logging
import sys

from cmdserver import cmd_server
from config import server_address
from ledz import led_controller
from musicplayer import music_play
from head_knife import head_knife
from vines import vines
from timerrr import timerrr
from servo_timer import servo_timer

logging.basicConfig(
    level=logging.DEBUG,
    format='%(name)s: %(message)s',
    stream=sys.stderr,
)
log = logging.getLogger('main')


class state():
    led_stage = 'RAND'  # toggle between RAND, SYNC and STEADY
    head_servo_stage = 'NOD'  # toggle between NOD and TURN
    carve_servo_stage = 'ROUND'  # toggle between ROUND and STAB
    vines_stage = 'STILL' # toggle between STILL and SHAKE
    loop = None

def main(args):

    loop = asyncio.get_event_loop()
    global_state = state()
    global_state.loop = loop

    factory = functools.partial(cmd_server, global_state)
    cmd_receiver = loop.create_server(factory, *server_address)

    loop.run_until_complete(cmd_receiver)
    log.debug('Listening for commands on {} port {}'.format(*server_address))

    if args.music:
        musicfinished_future = loop.run_in_executor(None, music_play)

    if args.servo:
        asyncio.ensure_future(head_knife_servo(global_state))
        asyncio.ensure_future(vines_servo(global_state))

    asyncio.ensure_future(led_controller(global_state, 19))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
            pass
    finally:
        log.debug('closing event loop')
        loop.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pumpkin Patchoulli "
                                                 "Pip Pip Pop Pickers!")
    parser.add_argument("-s", "--servo", help="Run the servo controller code",
                        action="store_true")

    parser.add_argument("-m", "--music", help="Run the music and timer controller",
                        action="store_true")

    args = parser.parse_args()

    main(args)
