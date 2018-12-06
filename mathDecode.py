import numpy as np
import matplotlib.pyplot as plt
import string


DURATION = round(2*np.pi)
LENGTH = 6
FREQ_LIST = []
for i in range(LENGTH):
    FREQ_LIST.append((i+1)*np.pi)



min = 1
max = 26

AMP_DICT = {'0':0, ' ':0}
alphabet = string.ascii_lowercase
amps = np.linspace(min, max, 26)
for i in range(len(alphabet)):
    AMP_DICT[alphabet[i]]=amps[i]
for i in range(len(string.punctuation)):
    AMP_DICT[string.punctuation[i]] = 0

INV_AMP_DICT = {v: k for k, v in AMP_DICT.items()}

def Riemann(signal, ts, bound):
    """
    signal is our discrete function (air pressure as a function of time), bound is the domain we are "integrating" over
    """
    t1, t2 = bound
    dx = DURATION/(len(ts)-1)
    print(dx)
    start_index = int(t1/dx)
    stop_index = int(t2/dx)

    total = 0
    print(signal)
    for i in range(start_index, stop_index):
        total += dx * signal[i]
    return total



def pure_sine(amp, freq):
    ts = np.linspace(0, DURATION, (5000*(DURATION))+1)
    sine = []
    for i in range(len(ts)):
        sine.append(amp*np.sin(ts[i]*freq))
    return sine


def Coefficient(signal, freq, domain=(0, 1)):
    """
    Trusts that the input has pi in it
    """
    ts = np.linspace(0, DURATION, (5000*(DURATION))+1)
    sine = pure_sine(1, freq)
    b = (2/DURATION) * Riemann(np.multiply(signal, sine), ts, domain)
    return b





def decode(signal):
    amps = []
    message = ''
    for i in range(len(FREQ_LIST)):
        amps.append(Coefficient(signal, FREQ_LIST[i], domain=(0, DURATION))) # TODO: make this not this way
        message = message + INV_AMP_DICT[round(amps[i])]
    # print("For frequencies:", FREQ_LIST)
    # print("Resulting amplitudes:", amps)
    # print("Fraction:", amp/amps[1])
    print(message)


# signal = np.add(pure_sine(5,np.pi), pure_sine(8, 2*np.pi))
signal = np.load("signal.npy")
decode(signal[0])
# for i in range(1, 28):
#     print("Amplitude:", i)
#     signal = pure_sine(i, 2*np.pi)
#     decode(signal, i)
