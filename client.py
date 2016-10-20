#!/usr/bin/env python
# needs python3 for asyncio

import argparse
import asyncio
import functools
import logging
import sys

logging.basicConfig(
    level=logging.DEBUG,
    format='%(name)s: %(message)s',
    stream=sys.stderr,
)
log = logging.getLogger('main')


SERVER_ADDRESS = ('localhost', 10000)

MESSAGES = [
    b'PING'
]


class AlleyClient(asyncio.Protocol):

    def __init__(self, messages, future):
        super().__init__()
        self.messages = messages
        self.log = logging.getLogger('AlleyClient')
        self.f = future

    def connection_made(self, transport):
        self.transport = transport
        self.address = transport.get_extra_info('peername')
        self.log.debug(
            'connection to {} port {}'.format(*self.address)
        )
        for msg in self.messages:
            transport.write(msg)
            self.log.debug('sending {!r}'.format(msg))
        if transport.can_write_eof():
            transport.write_eof()

    def data_received(self, data):
        self.log.debug('received {!r}'.format(data))

    def eof_received(self):
        self.log.debug('received EOF (client)')
        self.transport.close()
        if not self.f.done():
            self.f.set_result(True)

    def connection_lost(self, exc):
        self.log.debug('server close connection')
        self.transport.close()
        if not self.f.done():
            self.f.set_result(True)
        super().connection_lost(exc)


async def blinky_lights():
    for i in range(0, 5):
        print("I'm a wee LED light blinking - blinking randomly")
        await asyncio.sleep(3)
        # time.sleep(3)
    return 'task finished'


def main(master_mode=True):

    if master_mode:
        log.debug("Running in default client mode")
    else:
        log.debug("Running in client mode")

    loop = asyncio.get_event_loop()

    # factory = loop.create_server(AlleyServer, *SERVER_ADDRESS)
    # server = loop.run_until_complete(factory)
    # log.debug('starting up on {} port {}'.format(*SERVER_ADDRESS))

    client_completed = asyncio.Future()
    client_factory = functools.partial(
        AlleyClient,
        messages=MESSAGES,
        future=client_completed,
    )
    factory_coroutine = loop.create_connection(
        client_factory,
        *SERVER_ADDRESS
    )

    loop.run_until_complete(factory_coroutine)
    loop.run_until_complete(client_completed)

    try:
        loop.run_forever()
    finally:
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
