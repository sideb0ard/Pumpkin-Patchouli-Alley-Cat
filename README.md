# Pumpkin-Patchouli-Alley-Cat

Add raspberry pi addresses to 'nodes' in config.py

Run one node as the master with `./main -m`

Run worker nodes with default options `./main.py`

Everything runs from asyncio event loop - led controllers, servo controllers, and a TCP server to accept commands, which are used to change states, e.g. switch led controller mode from random to steady, switch servo mode from up and down to sideways etc.





