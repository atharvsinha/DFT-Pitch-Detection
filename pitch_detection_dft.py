import sounddevice as sd
import numpy as np
import os
import math 
import matplotlib.pyplot as plt
import librosa

total_input = []
sr = 44100 # sample frequency 
window = sr//2 # fft window size
step =  window//4 # step size for fft window
win_samples = [0]*window
standard_pitch = 440

# The sounddecive callback functionf fetches the input data for each window

def callback(indata, frames, time, status):
  global win_samples
  if status:
    print(status)
  if any(indata):
    win_samples = np.concatenate((win_samples,indata[:, 0])) # append new samples
    win_samples = win_samples[len(indata[:, 0]):] # remove old samples
    win_magnitude = abs(np.fft.fft(win_samples)[:window//2] )

    max_index = np.argmax(win_magnitude)
    maxFreq = max_index * (sr/window)
    i = int(np.round(math.log(maxFreq/standard_pitch, 2)*12))
    actual_pitch = standard_pitch*2**(i/12)
    op_note = librosa.hz_to_note(maxFreq)
    os.system('cls' if os.name=='nt' else 'clear')
    print(f"Closest note: {op_note} {maxFreq:.1f}/{actual_pitch:.1f}")
    
    total_input.append(actual_pitch)
  else:
    print('no input')

# Start the microphone input stream
try:
  with sd.InputStream(channels=1, callback=callback, blocksize=step, samplerate=sr):
    while True:
        if input()=='':
            break

except Exception as e:
    print(str(e))
plt.plot(total_input)
plt.show()
