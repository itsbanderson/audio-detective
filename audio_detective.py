# Adapted from the script described at 
# http://www.macdevcenter.com/pub/a/python/2001/01/31/numerically.html

import sys

# loading audio
from scikits import audiolab

# processing data
import numpy as np
from numpy.fft import rfft, fft
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

    n_out_pts = (fft_length / 2) + 1
    axis_hz = 0.5 * float(sample_rate) / n_out_pts * np.arange(n_out_pts)
    axis = axis_hz / 1000

    audio = []
    audionorm = []
    trans = freq_pwr.transpose()
    for freq in trans:
        audio.append(freq.sum())
        audionorm.append(freq.sum() / n_out_pts)

    #plt.plot(axis, audionorm)

    window = [-1, 0, 1]
    slope = np.convolve(audio, window, mode='same') / np.convolve(range((fft_length / 2) + 1), window, mode='same')

    slopes = []
    slopenorm = []
    for point in slope:
        slopes.append(point)
        slopenorm.append(point / n_out_pts)

    #plt.plot(axis, slopenorm)
    #plt.show()

    highfreq = 0
    for hz in axis_hz:
        if hz > highfreq:
            highfreq = hz
    freqinc = highfreq / ((fft_length / 2) + 1)
    freqcut = int(10000 / freqinc)
    slopespart = slopenorm[freqcut:]

    # Find local minima
    localminima = []
    for i in range(len(slopespart) - 2):
        if slopespart[i] > slopespart[i + 1] and slopespart[i + 1] < slopespart[i + 2] and slopespart[i + 1] < -10:
            localminima.append(slopespart[i + 1])

    if len(localminima) < 1:
        return "xxxxx"

    last = slopenorm.index(localminima[-1]) * freqinc
    if last > 20500:
        last = slopenorm.index(localminima[-2]) * freqinc

    lastround = round(last / 500) * 500
    bitfreqs = {20000: '320', 19500: '256', 19000: 'v0', 18500: '192', 18000: 'v2', 16500: '128'}
    #print last, lastround
    #print "Best guess at source quality: " + bitfreqs[lastround]
    return str(int(lastround)) + " - " + str(int(last))

if __name__ == "__main__":
    filename = sys.argv[1]
    fft_length = 2**int(sys.argv[2])
    get_spectrogram(filename, fft_length)
