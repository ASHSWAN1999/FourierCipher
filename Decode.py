from scipy.io.wavfile import read
import matplotlib.pyplot as plt
import numpy
import pyaudio
import wave
from mathDecode import Riemann

# GLOBAL VARIABLES
LENGTH = 6
FREQS_LIST = [] # The list of frequencies we care about, assigns each one to a position in the message
for i in range(LENGTH):
    FREQS_LIST.append(((i*10)+40)*2*np.pi)
#FREQS_LIST = [150.8, 176.6, 216, 253.1, 313.7, 412] # For nice music

DURATION = 2*np.pi/FREQS_LIST[0] * 20

CHAR_LIMIT = 200

START_TONE = 600
END_TONE = 650

RECORD_SEC = 12


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
                    CHUNK = 1024, RECORD_SECONDS=12):
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

def pure_sine(amp, freq):
    """
    Given an amplitude and a frequency, generates an array that contains discrete
    values from a sine wave of that amplitude and frequency
    """
    ts = np.linspace(0, DURATION, (8000*DURATION)+1)
    sine = []
    for i in range(len(ts)):
        sine.append(amp*np.sin(ts[i]*freq))
    return sine

def coefficient(signal, freq, domain=(0, 1)):
    """
    Calculates Fourier coefficient of the signal at a given frequency. This
    coefficient corresponds to the amplitude of the decomposed wave at this
    frqeuncy, which corresponds to a letter.
    """
    ts = np.linspace(0, DURATION, (8000*DURATION)+1)
    sine = pure_sine(1, freq)
    b = (2/DURATION) * Riemann(np.multiply(signal, sine), ts, domain)
    return b

def graph_wave(filename="rec.wav"):
    a = get_np_array(filename)
    t = len(a)
    ts = numpy.linspace(0, t, t)
    plt.plot(ts, a)
    plt.show()

def get_np_array(filename="rec.wav"):
    a = read(filename)
    a = numpy.array(a[1],dtype=float)
    return a

def find_start(signal):
    rate = 8000
    amps = []
    for i in range(len(signal)/2):
        amps[i] = coefficient(signal[i:], START_TONE, domain=(0, 1))
    start = amps.index(max(amps))
    return start + rate

def find_end(signal):
    amps = []
    for i in range(len(signal)-8000):
        amps[i] = coefficient(signal[i:], END_TONE, domain=(0, 1))
    stop = amps.index(max(amps))
    return stop



def process_file(filename="rec.wav"):
    signal = get_np_array(filename)
    start_index = find_start(signal)
    print(start_index)
    end_index = find_end(signal)
    print(end_index)
    return signal[start_index:end_index]

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


record_to_file(filename='rec.wav', RECORD_SECONDS=6)
graph_wave()
signal = process_file()

t = len(signal)
ts = numpy.linspace(0, t, t)
plt.plot(ts, signal)
plt.show()
