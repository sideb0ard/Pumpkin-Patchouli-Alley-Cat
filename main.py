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
#from servoz import servo_controller
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

def main(host=None, master_mode=False):

    loop = asyncio.get_event_loop()

    global_state = state()

    if host:
       listen_address = (host, 10000)
    else:
       listen_address = server_address  # from config.py

    factory = functools.partial(cmd_server, global_state)
    cmd_receiver = loop.create_server(factory, *listen_address)

    loop.run_until_complete(cmd_receiver)
    log.debug('Listening for commands on {} port {}'.format(*server_address))

    # for p in range(10):
    asyncio.ensure_future(led_controller(global_state, 19))
    asyncio.ensure_future(head_knife(global_state))
    asyncio.ensure_future(vines(global_state))

    if master_mode:
        print('I am the mastah')
    #    asyncio.ensure_future(timerrr(loop))
        asyncio.ensure_future(servo_timer(loop))

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
    parser.add_argument("-m", "--master", help="Run in Master mode",
                        action="store_true")

    parser.add_argument("-l", "--listen", dest="host",
                        help="Listen on specific IP addres")

    args = parser.parse_args()

    if args.master:
        main(args.host, master_mode=True)
    else:
        main(args.host)
