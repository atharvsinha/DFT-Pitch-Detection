import numpy as np
import librosa

notes = []
filename = input('Enter name of wav file:')
y, sr = librosa.load(filename)
window = sr//2 # fft window size
step =  window//2 # step size for fft window
for c in range(0, len(y), step):
  i  = int(np.argmax(abs(np.fft.fft(y[c:c+step])[:step])))
  try:
    notes.append(librosa.hz_to_note(i))
  except:
    pass

print(notes)
