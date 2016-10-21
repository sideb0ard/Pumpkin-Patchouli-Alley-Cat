import asyncio

from config import nodes

async def send_cmd(loop, host, cmd):
    print('Sending {} to {}'.format(cmd, host))
    reader, writer = await asyncio.open_connection(
        host, 10000, loop=loop)
    writer.write(cmd.encode())

    print('Close the socket')
    writer.close()


async def timerrr(loop):
    print('Timerd launched')
    while True:
        print('ARF!')
        print('Stage One - random lights')
        for node in nodes:
            await send_cmd(loop, node, 'LIGHTS')
        await asyncio.sleep(3)

        print('Stage Two - SOLID lights')
        for node in nodes:
            await send_cmd(loop, node, 'CAMERA')
        await asyncio.sleep(3)

        print('Stage THREE - SCARECROW')
        for node in nodes:
            await send_cmd(loop, node, 'ACTION')
        await asyncio.sleep(3)
