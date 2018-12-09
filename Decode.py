from scipy.io.wavfile import read
import matplotlib.pyplot as plt
import numpy
import pyaudio
import wave
from mathDecode import Riemann, pure_sine, coefficient

# GLOBAL VARIABLES
DURATION = round(2*np.pi) # Sets length of time for each "sound wave"
LENGTH = 50 # Sets length of time for each "sound wave"
FREQ_LIST = [] # The list of frequencies we care about, assigns each one to a position in the message
for i in range(LENGTH):
    FREQ_LIST.append((i+1)*np.pi)

AMP_DICT = {'0':0, ' ':0} # Maps each letter to the corresponding amplitude
alphabet = string.ascii_lowercase
amps = np.linspace(1, 26, 26)
for i in range(len(alphabet)):
    AMP_DICT[alphabet[i]]=amps[i]
for i in range(len(string.punctuation)):
    AMP_DICT[string.punctuation[i]] = 0

INV_AMP_DICT = {v: k for k, v in AMP_DICT.items()} # Inverts dictonary for decoding
INV_AMP_DICT[0] = ' '

def record_to_file(filename,FORMAT = pyaudio.paInt16, CHANNELS = 1, RATE = 8000,
                    CHUNK = 1024, RECORD_SECONDS=1):
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

def get_chunks(signal):
    rec_rate = RECORD_SECONDS/len(signal)
    num_chunks = len(message)/LENGTH
    while len(signal) < DURATION * num_chunks

def decode(filename="rec.wav"):
    """
    Iterates through the list of signals and decomposes each to an amplitudes and
    frequencies, which it converts back to text. Returns the concatenated string.
    """
    signal = get_np_array(filename)

    message = ''
    for i in range(len(signal)):
        chunk = signal[i]
        for j in range(len(FREQ_LIST)):
            amp = coefficient(chunk, FREQ_LIST[j], domain=(0, DURATION)) # TODO: make this not this way
            message = message + INV_AMP_DICT[round(amp)]
    return message


record_to_file(filename='rec.wav', RECORD_SECONDS=6)
graph_wave()
