# -*- coding: utf-8 -*-
"""
Created on Sat Jul  8 13:00:43 2023

@author: Usuario
"""

from scipy import signal
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt

def spect(montage):
    """
    Compute the continuous wavelet transform using complex Morlet Wavelet

    Parameters
    ----------
    montage : ndarray
        EEG montages.

    Returns
    -------
    time : ndarray
        time array.
    freqs : ndarray
        frequency array.
    power : ndarray
        power spectrum array.

    """
    fs = 250
    sampling_period = 1/fs
    frequency_band = [1, 30]
    frequencies = np.arange(frequency_band[0], frequency_band[1]+0.1, 0.1)
    # Compute scales
    #scales = 1/(frequencies*sampling_period)
    time_seconds = 5
    f, t, Sxx = signal.spectrogram(montage[:fs*time_seconds], fs)
    #[coef, freqs] = pywt.cwt(montage[:fs*time_seconds], scales,'cmor1.0-1.0', sampling_period)
    #power = (np.abs(coef))**2
    return Sxx


    