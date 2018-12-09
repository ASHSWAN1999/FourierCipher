from psonic import *
import numpy as np
import string


LENGTH = 6
FREQS_LIST = [] # The list of frequencies we care about, assigns each one to a position in the message
for i in range(LENGTH):
    FREQS_LIST.append(((i*10)+40)*2*np.pi)
#FREQS_LIST = [150.8, 176.6, 216, 253.1, 313.7, 412] # For nice music

DURATION = 2*np.pi/FREQS_LIST[0] * 20

CHAR_LIMIT = 200

START_TONE = 1000
END_TONE = 1100

min_vol = 0.5
max_vol = 2


AMP_DICT = {'0':0, ' ':0}
alphabet = string.ascii_lowercase
amps = np.linspace(1, 26, 26)
for i in range(len(alphabet)):
    AMP_DICT[alphabet[i]]=amps[i]
for i in range(len(string.punctuation)):
    AMP_DICT[string.punctuation[i]] = 0

SCALE = (max_vol-min_vol)/26

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
    while len(message) > CHAR_LIMIT:
        message = (input("Fewer than %s characters, please\n"%CHAR_LIMIT))
        message = message.lower()

    volumes = [None]*LENGTH #  Will be used to tell play_list what to play

    play(freq_to_midi(START_TONE), amp=2, attack=0, sustain=DURATION, release=0) #Start tone
    sleep(DURATION)
    while len(message) > LENGTH: # Keep going through chunks of the message
        for i in range(LENGTH): # In each chunk, convert each letter to an amplitude and store it
            volumes[i] = AMP_DICT[message[i]]*SCALE
        #print(message[:6])
        play_list(volumes) # Play one chunk
        message = message[LENGTH:] # Cut the played section out
        #print(message)
    if len(message) > 0: # Afterwords, play the remainder
        message = message + '0'*(LENGTH-len(message))
        #print(message)
        volumes = [None]*LENGTH
        for i in range(len(message)):
            volumes[i] = AMP_DICT[message[i]]*SCALE
        play_list(volumes)

    play(freq_to_midi(END_TONE), amp=2, attack=0, sustain=DURATION, release=0)
    sleep(DURATION)


if __name__ == "__main__":
    signals = message_to_sound()
