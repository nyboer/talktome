# Pocketsphinx on CHIP

The `mictotext.py` script is a very simple example of using speech to text on CHIP.
 * employs a limited dictionary of ~100+ words
 * records from a mic
 * converts the audio to text using pocketsphinx
 * looks for spoken numbers 0-9
 * recites any numbers decoded from the speech using WAV files

You'll need to install and build several things to get this running. First, you can install various dependencies with apt-get:
	sudo apt-get install -y git libtool autoconf automake bison python-dev make pkg-config build-essential curl python-pip swig python-pyaudio

Once those are finished, you'll have to build and install sphinxbase and pocketsphinx. It is straightforward, but does take some time. Not all day, but long enough that you can forget it's happening:

Install sphinxbase:

```
git clone https://github.com/cmusphinx/sphinxbase.git
cd sphinxbase	
./autogen.sh
./configure
make
make install
```

Install pocketsphinx library

```
git clone https://github.com/cmusphinx/pocketsphinx.git
./autogen.sh
./configure
make clean all
sudo make install
```

(libraries are installed into /usr/local/lib)

Install [pocketsphinx for python](https://github.com/cmusphinx/pocketsphinx-python)
	pip install pocketsphinx
	
Now run 
```
python mictotext.py
```
When you hear "TALK", say some numbers into the microphone. It will stop recording after 5 seconds or so, then crunch away at the audio to extract words. Once that is complete, it will "speak" the words back to you.

There are also a couple other example scripts. `basic.py` is just a slightly modified example from the pocketsphinx-python repo. `pyaud_rec.py` is an example of recording audio using pyaudio.

## Credit
Speak and spell samples found from http://www.maximporges.com/2011/10/08/speak-and-spell-samples/