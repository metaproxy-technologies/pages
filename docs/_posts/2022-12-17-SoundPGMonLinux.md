---
title: "Sound settings for console programming in Linux"
date: 2022-12-17
classes: wide
---

Everytime I am going to try something SOUND related in Linux, struggle starts, because of my lack of knowledge.
I have wasted tons of seconds, so I will share lessons learned to you ( and myself in the future ).

## Check to see if recording and playing works

You felt strange ser? Yes this is basic, but we are too used to be in hand of Microsoft and Apple and Google,
so we are expecting recording and playing is as granted, but here is land of opensource, so you need to VERIFY.

```bash
speaker-test -t wav
arecord --format=S16_LE --duration=5 --rate=16000 --file-type=raw out.raw
aplay --format=S16_LE --rate=16000 out.raw
```

Have you heard your voice recorded? If not, try to search until you get result.

Reference is: <https://developers.google.com/assistant/sdk/guides/library/python/embed/audio?hardware=ubuntu>

## Retrieve device index

I guess some of you have experienced like this when you try to use PyAudio.
This is because you ( including me ) are ignorant to specify proper hardware index.

```bash
ALSA lib pcm_dsnoop.c:641:(snd_pcm_dsnoop_open) unable to open slave
ALSA lib pcm_dmix.c:1089:(snd_pcm_dmix_open) unable to open slave
ALSA lib pcm.c:2642:(snd_pcm_open_noupdate) Unknown PCM cards.pcm.rear
ALSA lib pcm.c:2642:(snd_pcm_open_noupdate) Unknown PCM cards.pcm.center_lfe
ALSA lib pcm.c:2642:(snd_pcm_open_noupdate) Unknown PCM cards.pcm.side
ALSA lib pcm_oss.c:377:(_snd_pcm_oss_open) Unknown field port
ALSA lib pcm_oss.c:377:(_snd_pcm_oss_open) Unknown field port
ALSA lib pcm_usb_stream.c:486:(_snd_pcm_usb_stream_open) Invalid type for card
ALSA lib pcm_usb_stream.c:486:(_snd_pcm_usb_stream_open) Invalid type for card
ALSA lib pcm_dmix.c:1089:(snd_pcm_dmix_open) unable to open slave
Expression 'parameters->channelCount <= maxChans' failed in 'src/hostapi/alsa/pa_linux_alsa.c', line: 1514
Expression 'ValidateParameters( inputParameters, hostApi, StreamDirection_In )' failed in 'src/hostapi/alsa/pa_linux_alsa.c', line: 2818
Traceback (most recent call last):
  File "YOURCODE.py", line 15, in <module>
    stream = audio.open(format = form_1,rate = samp_rate,channels = chans, \
  File "/usr/local/lib/python3.8/dist-packages/pyaudio.py", line 754, in open
    stream = Stream(self, *args, **kwargs)
  File "/usr/local/lib/python3.8/dist-packages/pyaudio.py", line 445, in __init__
    self._stream = pa.open(**arguments)
OSError: [Errno -9998] Invalid number of channels
```

Try this:

```python
import pyaudio
import wave 

def main():
    audio = pyaudio.PyAudio()

    for x in range(0, audio.get_device_count()): 
        print(audio.get_device_info_by_index(x))

if __name__ == '__main__':
    main()
```

(Quoted from: <https://algorithm.joho.info/programming/python/pyaudio-device-index/>)

I guess in your output, you will see index number with maxInpurChennels>=1.
That's the number of indexes you need to use.

```bash
{'index': 9, 'structVersion': 2, 'name': 'default', 'hostApi': 0, 'maxInputChannels': 32, 'maxOutputChannels': 32, 'defaultLowInputLatency': 0.008707482993197279, 'defaultLowOutputLatency': 0.008707482993197279, 'defaultHighInputLatency': 0.034829931972789115, 'defaultHighOutputLatency': 0.034829931972789115, 'defaultSampleRate': 44100.0}
```


## Use the index you have retrieved.

Almost done. Change the dev_index in the following code and run.
You'll see a wav file so confirm it includes your voice of Wow!

```python
import pyaudio
import wave

form_1 = pyaudio.paInt16 # 16-bit resolution
chans = 1 # 1 channel
samp_rate = 44100 # 44.1kHz sampling rate
chunk = 4096 # 2^12 samples for buffer
record_secs = 3 # seconds to record
dev_index = 2 # device index found by p.get_device_info_by_index(ii)
wav_output_filename = 'test1.wav' # name of .wav file

audio = pyaudio.PyAudio() # create pyaudio instantiation

# create pyaudio stream
stream = audio.open(format = form_1,rate = samp_rate,channels = chans, \
                    input_device_index = dev_index,input = True, \
                    frames_per_buffer=chunk)
print("recording")
frames = []

# loop through stream and append audio chunks to frame array
for ii in range(0,int((samp_rate/chunk)*record_secs)):
    data = stream.read(chunk)
    frames.append(data)

print("finished recording")

# stop the stream, close it, and terminate the pyaudio instantiation
stream.stop_stream()
stream.close()
audio.terminate()

# save the audio frames as .wav file
wavefile = wave.open(wav_output_filename,'wb')
wavefile.setnchannels(chans)
wavefile.setsampwidth(audio.get_sample_size(form_1))
wavefile.setframerate(samp_rate)
wavefile.writeframes(b''.join(frames))
wavefile.close()
```

 (Quoted from: <https://makersportal.com/blog/2018/8/23/recording-audio-on-the-raspberry-pi-with-python-and-a-usb-microphone>)


## Some more tips.

I am going to add. If you have questions, please DM me on twitter.
<https://twitter.com/rtree>

Any conversations except for spamming, phishing, sharing seed phrases and recruiting pump groups
 are welcomed.
 
 

