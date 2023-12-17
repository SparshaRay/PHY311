import cv2
import matplotlib.pyplot as plt
import numpy as np

vidcap = cv2.VideoCapture('IMG_1117.MOV')
# print(vidcap)

success,image = vidcap.read()
# print(success)
frate = round(vidcap.get(cv2.CAP_PROP_FPS))

count = 0
intensity = []
coordinates = [570, 900]
# coordinates = [510, 980]

maxframe = 1000

while True:
    ret, frame = vidcap.read()
    count += 1
    if count > maxframe:
        break
    intensity.append(frame[*coordinates][2])
    

# plt.plot(intensity)
# plt.xlabel('Frame')
# plt.ylabel('Intensity')

x = intensity

w = np.fft.fft(x)
freqs = np.fft.fftfreq(len(x))

'''keep dis line''' #-------------------------------<<<<<<<<<<<<<<<<<<<<<
plt.plot(freqs[3:len(freqs)//2]*frate, abs(w)[3:len(w)//2], '-')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')



idx = np.argmax(np.abs(w)[2:len(w)//2])+2
freq = freqs[idx]
freq_in_hertz = abs(freq * frate)
print(freq_in_hertz)

plt.show()
