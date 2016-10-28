import asyncio 
import logging
import pyaudio
import socket
import time
import wave

from subprocess import call

log = logging.getLogger('musicplayer')

CHUNK = 1024
FILE = "/home/pi/Code/Pumpkin-Patchouli-Alley-Cat/media/lonelyjack.wav"

def send_music_has_started_message():
    print("Sending music message")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 10000))
    msg = "MUSICSTART"
    msg_len = len(msg)
    sent = sock.send(msg.encode())
    if sent == 0:
        raise RuntimeError("socket connection broken")

def music_play():

    call(["/home/pi/Code/Pumpkin-Patchouli-Alley-Cat/startpulse.sh"])

    wf = wave.open(FILE, 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format =
                    p.get_format_from_width(wf.getsampwidth()),
                    channels = wf.getnchannels(),
                    rate = wf.getframerate(),
                    output = True)
    
    data = wf.readframes(CHUNK)
    send_music_has_started_message()
    while True:
        stream.write(data)
        data = wf.readframes(CHUNK)
        
        if data == b'':
            print("Rewinding music track")
            wf.rewind()
            data = wf.readframes(CHUNK)
            send_music_has_started_message()
    
    stream.close()
    p.terminate()
