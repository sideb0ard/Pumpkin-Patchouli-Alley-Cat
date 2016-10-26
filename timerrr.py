import asyncio
import functools
import logging

from config import nodes

log = logging.getLogger('timerrr')

async def send_cmd(cmd):
    #  log.debug('Sending {} to {}'.format(cmd, host))
    print("YARSENDINGi {}".format(cmd))
    # for node in nodes:
    #     await send_cmd(loop, node, cmd)
    #     reader, writer = await asyncio.open_connection(
    #         host, 10000, loop=loop)
    #     writer.write(cmd.encode())
    #     writer.close()

def launcher(loop, cmd):
    print("Ah yeah, {}".format(loop))
    # loop.create_task(functools.partial(send_cmd, msg))
    loop.create_task(send_cmd(cmd))

async def timerrr(loop):
    log.debug('Timerd launched')
    loop.call_later(0.2, launcher, loop, "BUM")
    loop.call_later(2, launcher, loop, "TUM")
    loop.call_later(5, launcher, loop, "RUM")
    # while True:

    # #  log.debug('Stage One - lights start steady and get more random')
    # await asyncio.sleep(10)

    # for node in nodes:
    #     await send_cmd(loop, node, 'LED_SYNC')
    # await asyncio.sleep(10)

    # #  log.debug('Stage Two - SYNC signal,
    # #  lights become more and more in sync')
    # for node in nodes:
    #     await send_cmd(loop, node, 'LED_STEADY')
    # await asyncio.sleep(10)

    # #  log.debug('Stage THREE - SCARECROW')
    # for node in nodes:
    #     await send_cmd(loop, node, 'HEAD_NOD')
    #     await send_cmd(loop, node, 'CARVE_ROUND')
    # await asyncio.sleep(3)

    # #  log.debug('Stage FOUR - SCAREY CROW')
    # for node in nodes:
    #     await send_cmd(loop, node, 'HEAD_TURN')
    #     await send_cmd(loop, node, 'CARVE_STAB')
    # await asyncio.sleep(3)
