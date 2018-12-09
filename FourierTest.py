import numpy as np
import matplotlib.pyplot as plt


DURATION = 0.1


def Fourier_Coeff(signal, freq):
    """
    Gets the fourier coefficient for a given frequency. Maybe.
    """
    N = len(signal)
    total = 0
    for n in range(N):
        total += signal[n]* np.cos(2*np.pi*freq*n*(1/N))
    return total*2/N


def DFT(signal):
    """
    Maybe gives a whole discrete fourier transform
    """
    ts = np.linspace(0, DURATION, (500*(DURATION))+1)
    plt.plot(ts, signal)
    freqs = np.linspace(0, 4*np.pi, 1000)
    dft = []
    for i in range(len(freqs)):
        dft.append(Fourier_Coeff(signal, freqs[i]))
    print(min(dft))
    print(freqs[dft.index(min(dft))])
    plt.figure()

    plt.plot(freqs, dft)
    plt.show()




def pure_sine(amp, freq):
    ts = np.linspace(0, DURATION, (1000*(DURATION))+1)
    sine = []
    for i in range(len(ts)):
        sine.append(amp*np.sin(ts[i]*freq))
    return sine


def Riemann(signal, ts, bound):
    """
    signal is our discrete function (air pressure as a function of time), bound is the domain we are "integrating" over
    """
    t1, t2 = bound
    dx = DURATION/(len(ts)-1)
    start_index = int(t1/dx)
    stop_index = int(t2/dx)

    total = 0
    for i in range(start_index, stop_index):
        total += dx * signal[i]
    return total


def Coefficient(signal, freq, domain=(0, 1)):
    ts = np.linspace(0, DURATION, (1000*(DURATION))+1)
    sine = pure_sine(1, freq*np.pi)
    b = (2/DURATION) * Riemann(np.multiply(signal, sine), ts, domain)
    return b

ts = np.linspace(0, DURATION, (1000*(DURATION))+1)
signal = pure_sine(1, 565.486677)

freqs = np.linspace(0, 4*np.pi, 1000)
amps = []
for freq in freqs:
    amps.append(Coefficient(signal, freq, domain=(0,DURATION)))


print("Maximum amplitude: " + str(max(amps)))
print("Corresponding Frequency: " + str(freqs[amps.index(max(amps))]))

plt.plot(ts, signal)
plt.figure()
plt.plot(freqs, amps)
plt.show()


# ft = np.fft.fft(signal)
# freqs = np.linspace(0, 4*np.pi, 5001)
# plt.figure()
#
# plt.plot(freqs, ft)
# plt.show()
