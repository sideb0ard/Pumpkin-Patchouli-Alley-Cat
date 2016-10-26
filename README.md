# Pumpkin-Patchouli-Alley-Cat

Add raspberry pi addresses to 'nodes' in config.py

Run one node as the music player / timer with `./main -m`

Run one node as the servo controller / timer with `./main -s`

Run worker nodes with default options `./main.py`

All nodes run the LED controller code.

Everything runs from asyncio event loop - led controllers, servo controllers, and a TCP server to accept commands, which are used to change states, e.g. switch led controller mode from random to steady, switch servo mode from up and down to sideways etc.


Requires Pulseaudio for the audio. apt-get install it and run in background with 'pulseaudio -D'

