#!/usr/bin/env python
# needs python3 for asyncio

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

logging.basicConfig(
    level=logging.DEBUG,
    format='%(name)s: %(message)s',
    stream=sys.stderr,
)
log = logging.getLogger('main')


SERVER_ADDRESS = ('localhost', 10000)
CLIENTS = ['localhost']


def main(master_mode=False):

    loop = asyncio.get_event_loop()

    if master_mode:
        log.debug("Running in Cmd Master mode - this node "
                  "will command: {}".format("tbd"))

        print("[MAIN] Clients are {}".format(CLIENTS))
        timerrr.CLIENTS = CLIENTS
        asyncio.ensure_future(timerrr())
        # cmd_completed = asyncio.Future()
        # cmd_factory = functools.partial(
        #     CmdSender,
        #     messages=[b'PING'],
        #     future=cmd_completed,
        # )
        # factory_coroutine = loop.create_connection(
        #     cmd_factory,
        #     *SERVER_ADDRESS
        # )
        # loop.run_until_complete(factory_coroutine)
        # loop.run_until_complete(cmd_completed)

    else:
        # client mode runs a TCP server to accept new commands
        log.debug("Running in client mode")

    factory = loop.create_server(CmdReceiver, *SERVER_ADDRESS)
    server = loop.run_until_complete(factory)
    log.debug('starting up on {} port {}'.format(*SERVER_ADDRESS))

    asyncio.ensure_future(led_controller())
    asyncio.ensure_future(servo_controller())

    try:
        loop.run_forever()
    except KeyboardInterrupt:
            pass
    finally:
        if master_mode:
            log.debug('closing server')
            server.close()
            loop.run_until_complete(server.wait_closed())

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
