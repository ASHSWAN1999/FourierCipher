import numpy as np
import string
import matplotlib.pyplot as plt

DURATION = 2
LENGTH = 20
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



def pure_sine(amp, freq):
    ts = np.linspace(0, DURATION, (1000*(DURATION))+1)
    sine = []
    for i in range(len(ts)):
        sine.append(amp*np.sin(ts[i]*freq))
    return sine

def message_to_sine():
    message = (input("Please Enter Your Message\n"))
    message = message.lower()



    amps = np.zeros(LENGTH) #  Will be used to tell play_list what to play
    signals = []
    while len(message)>LENGTH:
        for i in range(LENGTH): # makes amps
            amps[i] = AMP_DICT[message[i]]
        print(amps)

        sig = np.zeros(1000*(DURATION)+1)
        for i in range(LENGTH): # makes sine waves
            sine = pure_sine(amps[i], FREQ_LIST[i])
            sig = np.add(sig, sine)

        signals.append(sig)
        message = message[LENGTH:]
        print(message)

    if len(message) > 0:
        message = message + '0'*(LENGTH-len(message))
        print(message)
        for i in range(LENGTH): # makes amps
            amps[i] = AMP_DICT[message[i]]
        print(amps)
        sig = np.zeros(1000*(DURATION)+1)
        for i in range(LENGTH): # makes sine waves
            sine = pure_sine(amps[i], FREQ_LIST[i])
            sig = np.add(sig, sine)

        signals.append(sig)

    return signals

if __name__ == "__main__":
    signals = message_to_sine()
    ts = np.linspace(0, DURATION, (1000*(DURATION))+1)
    for i in range(len(signals)):
        plt.figure()
        plt.plot(ts, signals[i])
    plt.show()
