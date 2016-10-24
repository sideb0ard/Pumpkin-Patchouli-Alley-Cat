import asyncio
import logging

from config import nodes

log = logging.getLogger('servo_timer')

async def send_cmd(loop, host, cmd):
    #  log.debug('Sending {} to {}'.format(cmd, host))
    reader, writer = await asyncio.open_connection(
        host, 10000, loop=loop)
    writer.write(cmd.encode())

    #  log.debug('Close the socket')
    writer.close()


async def servo_timer(loop):
    log.debug('servo timer launched')
    print('servo_timer')
    while True:

        print('knife slicing mode')
        for node in nodes:
            await send_cmd(loop, node, 'head_knife_round')
        await asyncio.sleep(120)

        print('knife stab mode')
        for node in nodes:
            await send_cmd(loop, node, 'head_knife_stab')
        await asyncio.sleep(45)

        print('vine shake mode')
        for node in nodes:
            await send_cmd(loop, node, 'vines_shake')
        await asyncio.sleep(5)

        print('vine still mode')
        for node in nodes:
            await send_cmd(loop, node, 'vines_still')
        await asyncio.sleep(160)
