import time
import pyaudio
import wave

CHUNK = 1024
FILE = "media/lonelyjack.wav"
# FILE = "media/yummyfur.wav"

def music_play(filename):
    # open the file for reading.
    wf = wave.open(FILE, 'rb')
    
    # create an audio object
    p = pyaudio.PyAudio()
    
    # open stream based on the wave object which has been input.
    stream = p.open(format =
                    p.get_format_from_width(wf.getsampwidth()),
                    channels = wf.getnchannels(),
                    rate = wf.getframerate(),
                    output = True)
    
    data = wf.readframes(CHUNK)
    while True:
        stream.write(data)
        # read data (based on the CHUNK size)
        data = wf.readframes(CHUNK)
        
        # play stream (looping from beginning of file to the end)
        if data == b'':
            print("Rewinding music track")
            # writing to the stream is what *actually* plays the sound.
            # stream.write(data)
            wf.rewind()
            data = wf.readframes(CHUNK)
    
    # cleanup stuff.
    stream.close()
    p.terminate()
