import asyncio
import logging

from config import nodes

log = logging.getLogger('timerrr')

async def send_cmd(loop, host, cmd):
    #  log.debug('Sending {} to {}'.format(cmd, host))
    reader, writer = await asyncio.open_connection(
        host, 10000, loop=loop)
    writer.write(cmd.encode())

    #  log.debug('Close the socket')
    writer.close()


async def timerrr(loop):
    log.debug('Timerd launched')
    while True:
        #  log.debug('Stage One - random lights')
        for node in nodes:
            await send_cmd(loop, node, 'LED_RAND')
        await asyncio.sleep(10)

        #  log.debug('Stage Two - SOLID lights')
        for node in nodes:
            await send_cmd(loop, node, 'LED_STEADY')
        await asyncio.sleep(3)

        #  log.debug('Stage THREE - SCARECROW')
        for node in nodes:
            await send_cmd(loop, node, 'HEAD_NOD')
            await send_cmd(loop, node, 'CARVE_ROUND')
        await asyncio.sleep(3)

        #  log.debug('Stage FOUR - SCAREY CROW')
        for node in nodes:
            await send_cmd(loop, node, 'HEAD_TURN')
            await send_cmd(loop, node, 'CARVE_STAB')
        await asyncio.sleep(3)
