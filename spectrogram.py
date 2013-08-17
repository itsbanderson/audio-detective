# Adapted from the script described at 
# http://www.macdevcenter.com/pub/a/python/2001/01/31/numerically.html

import sys

# loading audio
from scikits import audiolab

# processing data
import numpy as np
from numpy.fft import rfft, fft
import scipy as sp
from math import sin, pi, log10

# plotting
import matplotlib.pyplot as plt

def get_spectrogram(filename, fft_length):
    fp = audiolab.Sndfile(filename, 'r')
    sample_rate = fp.samplerate
    total_num_samps = fp.nframes

    num_fft = (total_num_samps / fft_length ) - 2
    # create temporary working array
    fft_buckets = np.zeros((num_fft, fft_length), float)
    channels = fp.channels

    # read in the data from the file
    for i in range(num_fft):
        frames = fp.read_frames(fft_length)
        if channels == 2:
            # TODO: figure out how to combine channels appropriately
            fft_buckets[i,:] = frames[:,0] - 128.0
        elif channels == 1:
            fft_buckets[i,:] = frames - 128.0
        else:
            raise Exception("Unsupported # of channels: %d" % channels)

    # Window the data
    fft_buckets = fft_buckets * np.hamming(fft_length)

    # Transform with the FFT, Return Power
    freq_pwr  = 10*np.log10(1e-20 + abs(rfft(fft_buckets, fft_length)))

    # Plot the result
    n_out_pts = (fft_length / 2) + 1
    y_axis_hz = 0.5 * float(sample_rate) / n_out_pts * np.arange(n_out_pts)
    y_axis = y_axis_hz / 1000
    x_axis = (total_num_samps / float(sample_rate)) / num_fft * np.arange(num_fft)
    plt.xlabel('Time (sec)')
    plt.ylabel('Frequency (kHz)')

    plt.pcolormesh(x_axis, y_axis, freq_pwr.transpose())
    plt.xlim([0,x_axis.max()])
    plt.ylim([0,y_axis.max()])
    plt.colorbar()
    plt.show()

if __name__ == "__main__":
    filename = sys.argv[1]
    fft_length = int(sys.argv[2])
    get_spectrogram(filename, fft_length)
