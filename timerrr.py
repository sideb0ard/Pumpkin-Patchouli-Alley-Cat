import asyncio
import functools
import logging

from config import nodes

log = logging.getLogger('timerrr')

async def send_cmd(loop, cmd):
    for node in nodes:
        log.debug('Sending {} to {}'.format(cmd, node))
        reader, writer = await asyncio.open_connection(
            node, 10000, loop=loop)
        writer.write(cmd.encode())
        writer.close()

def launcher(loop, cmd):
    loop.create_task(send_cmd(loop, cmd))

async def timerrr(loop):

    log.debug('Timerd launched')

    # Servo 1: Knife
    loop.call_later(0.0, launcher, loop, "KNIFE_SERVO_ON")  # full speed
    loop.call_later(120, launcher, loop, "KNIFE_SERVO_OFF")

    #  Servo 2: Vines
    loop.call_later(0.0, launcher, loop, "VINES_SERVO_ON")  # full speed
    loop.call_later(300, launcher, loop, "VINES_SERVO_OFF")

    #  Servo 3: Head Y axis (look up)
    loop.call_later(0.0, launcher, loop, "HEAD_Y_OFF") 
    loop.call_later(120, launcher, loop, "HEAD_Y_ON_FWD")  # full speed
    loop.call_later(123, launcher, loop, "HEAD_Y_OFF")
    loop.call_later(163, launcher, loop, "HEAD_Y_ON_RWD")
    loop.call_later(166, launcher, loop, "HEAD_Y_OFF")

    #  Servo 4: Head X axis (turn to side)
    loop.call_later(0.0, launcher, loop, "HEAD_X_OFF") 
    loop.call_later(120, launcher, loop, "HEAD_X_ON_FWD")  # full speed
    loop.call_later(123, launcher, loop, "HEAD_X_OFF")
    loop.call_later(162, launcher, loop, "HEAD_X_ON_RWD")  # full speed
    loop.call_later(165, launcher, loop, "HEAD_X_OFF")

    #  Lantern lights: 160 pins
    loop.call_later(0.0, launcher, loop, "LED_RAND")
    loop.call_later(58, launcher, loop, "LED_SYNC")
    loop.call_later(70, launcher, loop, "LED_STEADY")
    loop.call_later(120, launcher, loop, "LED_RAND")
    loop.call_later(134, launcher, loop, "LED_SYNC")
    loop.call_later(154, launcher, loop, "LED_STEADY")
    loop.call_later(169, launcher, loop, "LED_OFF")

    #  Face lights: 1 pin
    loop.call_later(0, launcher, loop, "FACE_LED_OFF") 
    loop.call_later(123, launcher, loop, "FACE_LED_ON") 
    loop.call_later(165, launcher, loop, "FACE_LED_OFF") 
