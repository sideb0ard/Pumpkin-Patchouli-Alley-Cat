import asyncio
from config import led_stage

async def led_controller():
    while True:
        print("I'm a wee LED light blinking - blinking {} randomly"
              .format(led_stage))
        # if blinky_mode == 1:
        #     sleepy_time = random.random() * 3
        # else:
        sleepy_time = 0.75
        # print("Sleeping for {}".format(sleepy_time))
        await asyncio.sleep(sleepy_time)
