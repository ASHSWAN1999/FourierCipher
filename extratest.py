from psonic import *
import numpy as np
def freq_to_midi(freq):
    midi = 69 + 12 * np.log2(freq/440)
    #print(midi)
    return midi


play(freq_to_midi(440), amp=1, attack=0, sustain=10, release=0)
