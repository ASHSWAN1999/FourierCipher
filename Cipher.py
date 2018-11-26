from psonic import *
import numpy as np
import string


# Makes amplitude dictionary
min = 1
max = 26
AMP_DICT = {}
alphabet = string.ascii_lowercase
amps = np.linspace(min, max, 26)
for i in range(len(alphabet)):
    AMP_DICT[alphabet[i]]=amps[i]

def freq_to_midi(freq):
    return 69 + 12 * np.log2(freq/440)


def message_to_sound():
    freqs = np.linspace(100, 700, 6)
    message = input("Please Enter Something, please no more than six letters for now\n")
    if len(message)>6:
        print("Fuck you.")
    else:
        if len(message) < 6:
            message = message + '0'*(6-len(message))
        print(message)
        # for i in range(len(freqs)):
        #     play(freq_to_midi):


if __name__ == "__main__":
    message_to_sound()
