"""
Asks for a message as input, then converts the message into a series of waves,
with each letter corresponding to an amplitude and the index of that letter
corresponding to a frequency.

Saves that wave to a numpy array file, which can be read by mathDecode.py
"""

import numpy as np
import string
import matplotlib.pyplot as plt



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

# FUNCTIONS
def pure_sine(amp, freq):
    """
    Given an amplitude and a frequency, generates an array that contains discrete
    values from a sine wave of that amplitude and frequency
    """
    ts = np.linspace(0, DURATION, (5000*round(DURATION))+1)
    sine = []
    for i in range(len(ts)):
        sine.append(amp*np.sin(ts[i]*freq))
    return sine

def message_to_sine():
    """
    Divides input message into several chunks of length LENGTH, then turns each
    chunk into a sum of pure sine waves representing one letter. Stores these
    sine waves in an array.
    """
    message = (input("Please Enter Your Message\n"))
    message = message.lower()

    amps = np.zeros(LENGTH) #Sets up numpy array for the amplitudes of one chunk
    signals = [] # Stores each sine wave
    while len(message)>LENGTH:
        for i in range(LENGTH):
            amps[i] = AMP_DICT[message[i]] #Converts a letter to an amplitude and stores for this chunk

        sig = np.zeros(5000*round(DURATION)+1) #sets up the signal for this chunk
        for i in range(LENGTH): # makes sine waves
            sine = pure_sine(amps[i], FREQ_LIST[i])
            sig = np.add(sig, sine) #Creates the signal by adding each letters sine wave

        signals.append(sig)
        message = message[LENGTH:]

    if len(message) > 0: # Encodes the remainder
        message = message + '0'*(LENGTH-len(message)) # Adds zeros until LENGTH
        for i in range(LENGTH): # makes amps
            amps[i] = AMP_DICT[message[i]]
        print(amps)
        sig = np.zeros(5000*round(DURATION)+1)
        for i in range(LENGTH): # makes sine waves
            sine = pure_sine(amps[i], FREQ_LIST[i])
            sig = np.add(sig, sine)

        signals.append(sig)

    return signals

if __name__ == "__main__":
    signals = message_to_sine()
    ts = np.linspace(0, DURATION, (5000*round(DURATION))+1)
    for i in range(len(signals)):
        plt.figure()
        plt.plot(ts, signals[i])
    plt.show()
    np.save("signal", signals)
