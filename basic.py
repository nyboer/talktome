#!/usr/bin/env python
from os import environ, path

from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *

MODELDIR = "model"
DATADIR = "test"
#DICT = "cmudict-en-us.dict"
DICT = "cheeper.dict"

# Create a decoder with certain model
config = Decoder.default_config()
config.set_string('-hmm', path.join(MODELDIR, 'en-us/en-us'))
config.set_string('-lm', path.join(MODELDIR, 'en-us/en-us.lm.bin'))
config.set_string('-dict', path.join(MODELDIR, 'en-us/'+DICT))
decoder = Decoder(config)

# Decode streaming data.
decoder = Decoder(config)
decoder.start_utt()
stream = open(path.join(DATADIR, 'count.wav'), 'rb')
while True:
  buf = stream.read(1024)
  if buf:
    decoder.process_raw(buf, False, False)
  else:
    decoder.end_utt()
    print ('Best hypothesis segments: ', [seg.word for seg in decoder.seg()])
    break
#decoder.end_utt()
#print ('Best hypothesis segments: ', [seg.word for seg in decoder.seg()])
