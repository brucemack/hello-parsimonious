import math
import numpy as np

N = 128
fs = 2000
f0 = 250
PI = 3.1415926
phi = 2 * PI * f0 / fs
w = 0

s = []
for t in range(0, N):
    s.append(math.cos(phi * t))

Sw = np.fft.fft(s)

for i in range(0, int(N / 2)):
    print(i, abs(Sw[i]))


