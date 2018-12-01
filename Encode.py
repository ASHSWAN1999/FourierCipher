from psonic import *
import numpy as np
import string


LENGTH = 6
# midis = [48, 51, 55, 58, 62, 67] This is for reference for the frequencies
FREQS_LIST = [150.8, 176.6, 216, 253.1, 313.7, 412] # For nice music
#FREQS_LIST = np.linspace(500, 800, LENGTH) # For horrible screeching sounds
#FREQS_LIST = [np.pi, 2*np.pi, 3*np.pi, 4*np.pi, 5*np.pi, 6*np.pi]
DURATION = 1


min = 0.2
max = 1.5


AMP_DICT = {'0':0, ' ':0}
alphabet = string.ascii_lowercase
amps = np.linspace(min, max, 26)
for i in range(len(alphabet)):
    AMP_DICT[alphabet[i]]=amps[i]
for i in range(len(string.punctuation)):
    AMP_DICT[string.punctuation[i]] = 0

def freq_to_midi(freq):
    midi = 69 + 12 * np.log2(freq/440)
    #print(midi)
    return midi

def play_list(amps):
    for i in range(len(amps)):
        play(freq_to_midi(FREQS_LIST[i]), amp=amps[i], attack=0, sustain=DURATION, release=0)

    sleep(DURATION)



def message_to_sound():
    message = (input("Please Enter Your Message\n"))
    message = message.lower()

    volumes = [None]*LENGTH #  Will be used to tell play_list what to play

    while len(message) > LENGTH: # Keep going through chunks of the message
        for i in range(LENGTH): # In each chunk, convert each letter to an amplitude and store it
            volumes[i] = AMP_DICT[message[i]]
        #print(message[:6])
        play_list(volumes) # Play one chunk
        message = message[LENGTH:] # Cut the played section out
        #print(message)
    if len(message) > 0: # Afterwords, play the remainder
        message = message + '0'*(LENGTH-len(message))
        #print(message)
        volumes = [None]*LENGTH
        for i in range(len(message)):
            volumes[i] = AMP_DICT[message[i]]
        play_list(volumes)



if __name__ == "__main__":
    signals = message_to_sound()
