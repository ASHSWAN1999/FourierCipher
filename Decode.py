from scipy.io.wavfile import read
import matplotlib.pyplot as plt
import numpy
import pyaudio
import wave

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

def graph_wave():
    a = read("rec.wav")
    a = numpy.array(a[1],dtype=float)
    t = len(a)
    ts = numpy.linspace(0, t, t)
    plt.plot(ts, a)
    plt.show()

record_to_file(filename='rec.wav', RECORD_SECONDS=6)
graph_wave()
