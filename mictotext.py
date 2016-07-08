#!/usr/bin/env python
from os import environ, path
from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *

import pyaudio
import wave
import sys

#constants for audio formats
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "convertthis.wav"
PLAY_DIR = "wavs/"
# audio object for recording
audio = pyaudio.PyAudio()

# reference: http://stackoverflow.com/questions/6951046/pyaudio-help-play-a-file
def playwav(filename):
    playwave = wave.open(filename, 'rb')

    # create an audio object
    p = pyaudio.PyAudio()

    # open stream based on the wave object which has been input.
    playback = p.open(format =
                    p.get_format_from_width(playwave.getsampwidth()),
                    channels = playwave.getnchannels(),
                    rate = playwave.getframerate(),
                    output = True)

    # read data (based on the CHUNK size)
    playdata = playwave.readframes(CHUNK)

    # play stream (looping from beginning of file to the end)
    while playdata != '':
        # writing to the stream is what *actually* plays the sound.
        playback.write(playdata)
        playdata = playwave.readframes(CHUNK)
    # cleanup stuff.
    playback.close()
    p.terminate()

playwav(PLAY_DIR+'SILENCE.wav')
playwav(PLAY_DIR+'WELCOME.wav')

# Setup pocketsphinx constants for speech recognition
MODELDIR = "model"
#DICT = "cmudict-en-us.dict"
DICT = "cheeper.dict"

# Create a decoder with certain model
config = Decoder.default_config()
config.set_string('-hmm', path.join(MODELDIR, 'en-us/en-us'))
config.set_string('-lm', path.join(MODELDIR, 'en-us/en-us.lm.bin'))
config.set_string('-dict', path.join(MODELDIR, 'en-us/'+DICT))
decoder = Decoder(config)

#Instruct user to begin:
playwav(PLAY_DIR+'TALK.wav')

# start Recording
stream = audio.open(format=FORMAT, channels=CHANNELS,rate=RATE, input=True,frames_per_buffer=CHUNK)
print "-------------recording-------------------"
frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)
print "................finished recording................"

# stop Recording
stream.stop_stream()
stream.close()
audio.terminate()

#create WAV file
waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(frames))
waveFile.close()

# Decode streaming data.
decoder = Decoder(config)
decoder.start_utt()
stream = open(WAVE_OUTPUT_FILENAME, 'rb')
while True:
  buf = stream.read(1024)
  if buf:
    decoder.process_raw(buf, False, False)
  else:
    decoder.end_utt()
    words = [seg.word for seg in decoder.seg()]
    print '================================================'
    print ('Best hypothesis segments: ', words)
    print '================================================'
    break

#now playback the numbers of any numbers spoken
playwav(PLAY_DIR+'SILENCE.wav')
nums = ['one','two','three','four','five','six','seven','eight','nine','zero']
for w in words:
    if w in nums:
        filename = PLAY_DIR+w+'.wav'
        playwav(filename)

playwav(PLAY_DIR+'SILENCE.wav')
playwav(PLAY_DIR+'YOUWIN.wav')
