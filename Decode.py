from scipy.io.wavfile import read
import matplotlib.pyplot as plt
import numpy as np
import pyaudio
import string
import wave
import time

# GLOBAL VARIABLES
LENGTH = 6
FREQS_LIST = [] # The list of frequencies we care about, assigns each one to a position in the message
for i in range(LENGTH):
    FREQS_LIST.append(((i*10)+40)*2*np.pi)
#FREQS_LIST = [150.8, 176.6, 216, 253.1, 313.7, 412] # For nice music

# DURATION = 2*np.pi/FREQS_LIST[0] * 20
DURATION = 3

CHAR_LIMIT = 200

START_TONE = 1000
END_TONE = 1100

RECORD_SEC = 3


min_vol = 0.5
max_vol = 2


AMP_DICT = {'0':0, ' ':0}
alphabet = string.ascii_lowercase
amps = np.linspace(1, 26, 26)
for i in range(len(alphabet)):
    AMP_DICT[alphabet[i]]=amps[i]
for i in range(len(string.punctuation)):
    AMP_DICT[string.punctuation[i]] = 0

SCALE = (max_vol-min_vol)/26

INV_AMP_DICT = {v: k for k, v in AMP_DICT.items()} # Inverts dictonary for decoding
INV_AMP_DICT[0] = ' '

def record_to_file(filename,FORMAT = pyaudio.paInt16, CHANNELS = 1, RATE = 8000,
                    CHUNK = 1024, RECORD_SECONDS=5):
    audio = pyaudio.PyAudio()

    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    # stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()

    waveFile = wave.open(filename, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()


def Riemann(signal, ts, bound):
    """
    signal is our discrete function (air pressure as a function of time), bound is the domain we are "integrating" over
    """
    t1, t2 = bound
    dx = ts[1]-ts[0]
    start_index = int(t1/dx)
    stop_index = int(t2/dx)

    total = 0
    for i in range(start_index, stop_index):
        total += dx * signal[i]
    return total

def pure_sine(amp, freq, sine_length):
    """
    Given an amplitude and a frequency, generates an array that contains discrete
    values from a sine wave of that amplitude and frequency
    """
    ts = np.linspace(0, DURATION, sine_length)
    sine = []
    for i in range(len(ts)):
        sine.append(amp*np.sin(ts[i]*freq))
    return sine

def coefficient(signal, freq, domain=(0, 1)):
    """
    Calculates Fourier coefficient of the signal at a given frequency. This
    coefficient corresponds to the amplitude of the decomposed wave at this
    frequency, which corresponds to a letter.
    """
    ts = np.linspace(0, DURATION, len(signal)+1)
    sine = pure_sine(1, freq, sine_length=len(signal))
    b = (2/(domain[1]-domain[0])) * Riemann(np.multiply(signal, sine), ts, domain)
    return b

def graph_wave(filename="rec.wav"):
    a = get_np_array(filename)
    t = len(a)
    ts = np.linspace(0, t, t)
    plt.plot(ts, a)

def get_np_array(filename="rec.wav"):
    a = read(filename)
    a = np.array(a[1],dtype=float)
    return a

def find_start(signal):
    rate = len(signal) /RECORD_SEC
    tone_length = round(rate * DURATION)
    amps = []
    for i in range(int(len(signal)/2)):
        amps.append(coefficient(signal[1*i:1*i+tone_length+1], START_TONE, domain=(0, DURATION), sine_length=tone_length, rate=rate))
    start = 1 * amps.index(max(amps))
    return start + tone_length

def find_end(signal):
    rate = len(signal) /RECORD_SEC
    tone_length = round(rate * DURATION)
    amps = []
    for i in range(int((len(signal)-rate)/1)):
        amps.append(coefficient(signal[i*1:i*1+tone_length+1], END_TONE, domain=(0, DURATION), sine_length=tone_length, rate=rate))
    stop = 1*amps.index(max(amps))
    return stop



def process_file(filename="rec.wav"):
    signal = get_np_array(filename)
    background = np.load("background_noise.npy")
    t = len(signal)
    background = background[:t]

    signal = np.add(signal, -background)
    return signal
    # print(t)
    # print(RECORD_SEC*8000)
    # start_index = find_start(signal)
    # print(start_index)
    # end_index = find_end(signal)
    # print(end_index)
    # return signal[start_index:end_index]

def decode(filename="rec.wav"):
    """
    Iterates through the list of signals and decomposes each to an amplitudes and
    frequencies, which it converts back to text. Returns the concatenated string.
    """
    signal = process_file(filename)

    message = ''
    for i in range(len(signal)):
        chunk = signal[i]
        for j in range(len(FREQ_LIST)):
            amp = coefficient(chunk, FREQ_LIST[j], domain=(0, DURATION)) # TODO: make this not this way
            message = message + INV_AMP_DICT[round(amp)]
    return message

def get_transform(signal, background_check=False, filter=False):
    amps = []
    freqs = []

    for i in range(10000):
        amps.append(coefficient(signal, 2*np.pi*i*0.1, domain = (0, DURATION)))
        freqs.append(i*0.1*2*np.pi)
    plt.plot(freqs, amps)
    plt.show()
    if background_check:
        np.save("background_noise", amps)

if __name__ == "__main__":
    record_to_file(filename='rec.wav', RECORD_SECONDS=1)
    signal = process_file()
    get_transform(signal)
    #
    # signal = process_file()

    # t = len(signal)
    #
    # ts = np.linspace(0, t, t)
    # graph_wave()
    # plt.figure()
    # plt.plot(ts, signal)
    # plt.show()
