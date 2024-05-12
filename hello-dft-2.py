import math
import numpy as np
import matplotlib.pyplot as plt

PI = 3.1415926
N = 128
fs = 2000

"""
Example 1: 
200 Hz sinusoid (zero-centered) multiplied by a 500 Hz square wave (zero-centered).
The result is energy at the sum and difference frequencies : 300 and 700 Hz.

Both signals are balanced so there is no feed-through of either signal.
"""
print("Example 1:")

f0 = 200
a0 = 0.25
f1 = 500
a1 = 1.0
w0 = 2 * PI * f0 / fs
phi0 = 0
w1 = 2 * PI * f1 / fs
phi1 = 0

sn = []
for n in range(0, N):

    # RF signal
    s0 = a0 * math.cos(phi0)
    phi0 = phi0 + w0

    # L0 (square wave)
    s1 = a1 * math.cos(phi1)
    if s1 > 0: 
        s1 = 1
    else:
        s1 = -1
    phi1 = phi1 + w1
    sn.append(s0 * s1)

Sw = np.fft.fft(sn)

for i in range(0, int(N / 2)):
    f = i * (fs / N)
    print("{:4d}".format(int(f)), "{:d}".format(int(abs(Sw[i]))))

"""
Example 2: This is an illustration of a single-balanced mixer.

A 200 Hz sinusoid (zero-centered) is multiplied by a 500 Hz square wave (Not zero-centered).
The result is energy at the sum and difference frequencies : 300 and 700 Hz.

Because the 500 Hz square wave is not centered we will also see leakage of 200 Hz.
"""
print("Example 2:")
f0 = 200
a0 = 0.25
f1 = 500
a1 = 1.0
w0 = 2 * PI * f0 / fs
phi0 = 0
w1 = 2 * PI * f1 / fs
phi1 = 0

sn = []
for n in range(0, N):

    # RF signal
    s0 = a0 * math.cos(phi0)
    phi0 = phi0 + w0

    # L0 (square wave)
    s1 = a1 * math.cos(phi1)
    if s1 > 0: 
        s1 = 1.5
    else:
        s1 = -0.5
    phi1 = phi1 + w1
    sn.append(s0 * s1)

Sw = np.fft.fft(sn)

for i in range(0, int(N / 2)):
    f = i * (fs / N)
    print("{:4d}".format(int(f)), "{:d}".format(int(abs(Sw[i]))))


"""
Example 3: Single-balanced mixer.

400 Hz RF sinusoid is added to a 1.0v bias.  This is switched back and 
forth by a 500 Hz square wave LO.
The result is energy at the sum and difference frequencies : 100 and 900 Hz.

Because the RF is not balanced we see huge leakage of the LO at 500 Hz.
"""
print("Example 3:")

f0 = 400
a0 = 0.25
f1 = 500
a1 = 1.0
w0 = 2 * PI * f0 / fs
phi0 = 0
w1 = 2 * PI * f1 / fs
phi1 = 0
t_bias = 1.4

sn = []
ta_n = []
tb_n = []

for n in range(0, N):

    # RF signal
    s0 = a0 * math.cos(phi0)
    phi0 = phi0 + w0

    # Compute the two branches
    s1 = a1 * math.cos(phi1)
    if s1 > 0: 
        ta = 1.8
        tb = t_bias + s0
    else:
        ta = t_bias + s0
        tb = 1.8

    phi1 = phi1 + w1
    ta_n.append(ta)
    tb_n.append(tb)
    sn.append(ta - tb)

Sw = np.fft.fft(sn)
freq = []
mag = []

for i in range(0, int(N / 2)):
    f = i * (fs / N)
    print("{:4d}".format(int(f)), "{:d}".format(int(abs(Sw[i]))))
    freq.append(f)
    mag.append(abs(Sw[i]))

plt.plot(freq, mag)

#plt.plot(ta_n)
#plt.plot(tb_n)
#plt.ylabel('some numbers')
plt.show()

