#!/usr/bin/env python
# needs python >= 3.5 for asyncio

import argparse
import asyncio
# import functools
import logging
# import signal
import sys

from cmdmessages import CmdReceiver
from servoz import servo_controller
from ledz import led_controller
from timerrr import timerrr

from config import server_address

logging.basicConfig(
    level=logging.DEBUG,
    format='%(name)s: %(message)s',
    stream=sys.stderr,
)
log = logging.getLogger('main')


def main(master_mode=False):

    loop = asyncio.get_event_loop()

    if master_mode:
        asyncio.ensure_future(timerrr(loop))

    factory = loop.create_server(CmdReceiver, *server_address)
    loop.run_until_complete(factory)
    log.debug('Listening for commands on {} port {}'.format(*server_address))

    asyncio.ensure_future(led_controller())
    asyncio.ensure_future(servo_controller())

    try:
        loop.run_forever()
    except KeyboardInterrupt:
            pass
    finally:
        # loop.run_until_complete(server.wait_closed())

        log.debug('closing event loop')
        loop.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pumpkin Patchoulli "
                                                 "Pip Pip Pop Pickers!")
    parser.add_argument("-m", "--master", help="Run in Master mode",
                        action="store_true")
    args = parser.parse_args()
    if args.master:
        main(master_mode=True)
    else:
        main()
