# -*- coding: utf-8 -*-


from scipy.signal import welch as pwelch
import numpy as np


def relative_powers(signal, fs=250, nperseg=500, noverlap=250, max_freq=50):
    """
    Power spectrum of EEG signal is calculated

    Parameters
    ----------
    signal : ndarray
        EEG time series.
    fs : int, optional
        sample frequency. The default is 250.
    nperseg : int, optional
        window size. The default is 500.
    noverlap : int, optional
        window overlap. The default is 250.
    max_freq : int, optional
        maximun frequency. The default is 50.

    Returns
    -------
    result : ndarray
        relative power spectrum of the EEG bands.
    total : ndarray
        total power spectrum of the EEG signal.

    """
    f, pxx = pwelch(signal, fs, 'hann', nperseg, noverlap)

    theta = np.sum(pxx[(f <= 8) & (f > 4)], axis=0)
    alpha = np.sum(pxx[(f <= 13) & (f > 8)], axis=0)
    beta = np.sum(pxx[(f <= 30) & (f > 13)], axis=0)
    gamma = np.sum(pxx[(f <= max_freq) & (f > 30)], axis=0)

    # Delta is not used
    total = np.sum(pxx[(f <= max_freq) & (f > 4)],axis=0)
    #total = pxx[(f <= max_freq) & (f > 4)]
    theta_relative = theta/total
    alpha_relative = alpha/total
    beta_relative = beta/total
    gamma_relative = gamma/total

    result = np.asarray([theta_relative, alpha_relative, beta_relative,
                         gamma_relative])


    return total, result
