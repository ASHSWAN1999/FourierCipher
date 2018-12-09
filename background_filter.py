
import numpy as np
import pyaudio

from Decode import RECORD_SEC, record_to_file, get_np_array




record_to_file(filename='background.wav', RECORD_SECONDS=RECORD_SEC+1)
signal = get_np_array(filename='background.wav')
np.save("background_noise", signal)
