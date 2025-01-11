import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

# Define filter parameters
numtaps = 31  # Number of filter coefficients
fs = 1000   # Sampling frequency (Hz)

# Design the filter
bands = [0.05 * fs / 2, 0.95 * fs / 2]  # Band edges
desired = [ 1 ]  # Desired gain response 
weights = [ 1 ]  # Weights for passband and stopband

h = signal.remez(numtaps, bands, desired, weight=weights, type="hilbert", fs=fs)

# Plot impulse response
plt.stem(h)
#plt.plot(h)
#plt.xlabel('n')
#plt.ylabel('Gain (Linear)')
#plt.title('Parks-McClellan Filter - Impulse Response')
#plt.grid(True)
plt.show()


# Plot the frequency response
w, h = signal.freqz(h)
plt.plot(w * (fs / (2 * np.pi)), 20 * np.log10(np.abs(h)))
plt.xlabel('Frequency (Hz)')
plt.ylabel('Gain (dB)')
plt.title('Parks-McClellan Filter')
plt.grid(True)
plt.show()

# Plot the phase response
w, h = signal.freqz(h)
plt.plot(w * fs / (2 * np.pi), np.angle(h))
plt.xlabel('Frequency (Hz)')
plt.ylabel('Phase')
plt.title('Parks-McClellan Filter (Phase)')
plt.grid(True)
plt.show()