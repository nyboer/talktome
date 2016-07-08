import pyaudio
import wave

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "py_record.wav"

audio = pyaudio.PyAudio()

# start Recording
stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK,input_device_index=2)


#get some info
print 'host api count '+str(audio.get_host_api_count())
print 'device count '+str(audio.get_device_count())
print 'input info '+str(audio.get_default_input_device_info())
print 'host info '+str(audio.get_default_host_api_info())
print 'device info 0 '+str( audio.get_device_info_by_index(0) )
print 'device info 1 '+str( audio.get_device_info_by_index(1) )
print 'device info 2 '+str( audio.get_device_info_by_index(2) )
print 'device info 3 '+str( audio.get_device_info_by_index(3) )
print 'device info 4 '+str( audio.get_device_info_by_index(4) )

print "recording..."
frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    #print 'chunk'
    data = stream.read(CHUNK)
    frames.append(data)
print "finished recording"


# stop Recording
stream.stop_stream()
stream.close()
audio.terminate()

waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(frames))
waveFile.close()
