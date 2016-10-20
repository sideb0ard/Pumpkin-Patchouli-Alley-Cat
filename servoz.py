import asyncio

async def servo_controller():

    movement = "nodding"
    while True:
        print("I'm a MOVING SERVO blinking - {}"
              .format(movement))
        sleepy_time = 0.5
        # print("Sleeping for {}".format(sleepy_time))
        await asyncio.sleep(sleepy_time)
