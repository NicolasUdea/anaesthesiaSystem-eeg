# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 08:48:46 2022

@author: Maria Camila Villa,Yeimmy Morales
"""

import numpy as np
import scipy.signal as signal


def firws(m, f, w, t=None):
    """
   Checks that filter order is a real, even, positive integer and
   frequencies fall in range between 0 and 1. Finally, calls the fkernerl
   function.

    Parameters
    ----------
    m : scalar or int
        filter order.
    f : scalar or numpy.ndarray
        cutoff frequency/ies (-6 dB;pi rad / sample).
    w : ndarray
        vector of length m + 1 defining window.
    t : string (optional)
        'high' for highpass, 'stop' for bandstop filter. The default is
        low-/bandpass.

    Returns
    -------
    b: ndarray
        filter coefficients.

    """
    try:
        m = int(m)
        if(m % 2 != 0) or (m < 2):
            print(type(m))
            print('Filter order must be a real, even, positive integer.')
            return False
    except (ValueError, TypeError):
        print('Filter order must be a real, even, positive integer.')
        return False

    if (not type(f) is np.ndarray):
        print('the variable f must be ndarray type.')
        return False

    f = np.squeeze(f)
    if (f.ndim > 1) or (f.size > 2):
        print('the variable f must be scalar or vector of two values.')
        return False
    f = f/2

    if np.any(f <= 0) or np.any(f >= 0.5):
        print('Frequencies must fall in range between 0 and 1.')
        return False

    w = np.squeeze(w)
    if (f.ndim == 0):
        b = fkernel(m, f, w)
    else:
        b = fkernel(m, f[0], w)
    if (f.ndim == 0) and (t == 'high'):
        b = fspecinv(b)
    elif (f.size == 2):
        b = b + fspecinv(fkernel(m, f[1], w))
        if t is None or t != 'stop':
            b = fspecinv(b)
    return b


def fkernel(m, f, w):
    """
    Computes the filter coefficients.

    Parameters
    ----------
    m : scalar or int
        filter order.
    f : scalar or numpy.ndarray
        cutoff frequency/ies (-6 dB;pi rad / sample).
    w : ndarray
        vector of length m + 1 defining window.

    Returns
    -------
    b: ndarray
        filter coefficients.

    """

    m = np.arange(-m/2, (m/2)+1)
    b = np.zeros((m.shape[0]))
    b[m == 0] = 2*np.pi*f  # No division by zero
    b[m != 0] = np.sin(2*np.pi*f*m[m != 0])/m[m != 0]  # Sinc
    b = b*w
    b = b/np.sum(b)  # Normalization to unity gain at DC
    return b


def fspecinv(b):
    """
    Compute the spectral inversion if it is a high or band-stop filter.

    Parameters
    ----------
    b : ndarray
        filter coefficients.

    Returns
    -------
    b : ndarray
        inverse filter coefficients.

    """
    b = -b
    b[int((b.shape[0]-1)/2)] = b[int((b.shape[0]-1)/2)]+1
    return b


def filter_design(fs, locutoff=0, hicutoff=0, revfilt=0):
    """
    Use the low-pass as the prototipical filter, compute the filter order
    and the cutoff frequencies. Finally, it calls the firws function.

    Parameters
    ----------
    locutoff : int, optional
        first cutoff frequency. The default is 0.
    hicutoff : int, optional
        second cutoff frequency. The default is 0.
    revfilt : int, optional
        if revfilt=1 inverts the logic for low-pass to high-pass
        and for band-pass to notch. The default is 0.

    Returns
    -------
    b: ndarray
        filter coefficients.
    filtorder: int
        filter order.

    """
    # Constants
    TRANSWIDTHRATIO = 0.25
    fNyquist = fs/2

    # The prototipical filter is the low-pass, we design a low pass and
    # transform it

    # Convert highpass to inverted lowpass
    if hicutoff == 0:
        hicutoff = locutoff
        locutoff = 0
        # invert the logic for low-pass to high-pass and for band-pass to notch
        revfilt = 1
    if locutoff > 0 and hicutoff > 0:
        edgeArray = np.array([locutoff, hicutoff])
    else:
        edgeArray = np.array([hicutoff])

    # Not negative frequencies and not frequencies above Nyquist
    if np.any(edgeArray < 0) or np.any(edgeArray >= fNyquist):
        print('Cutoff frequency out of range')
        return False

    # Max stop-band width
    maxBWArray = edgeArray.copy()  # Band-/highpass
    if revfilt == 0:  # Band-/lowpass
        maxBWArray[-1] = fNyquist-edgeArray[-1]
    elif len(edgeArray) == 2:  # Bandstop
        maxBWArray = np.diff(edgeArray)/2
    maxDf = np.min(maxBWArray)

    # Default filter order heuristic
    if revfilt == 1:  # Highpass and bandstop
        df = np.min([np.max([maxDf*TRANSWIDTHRATIO, 2]), maxDf])
    else:  # Lowpass and bandpass
        df = np.min([np.max([edgeArray[0]*TRANSWIDTHRATIO, 2]), maxDf])
    print(df)

    filtorder = 3.3/(df/fs)  # Hamming window
    filtorder = np.ceil(filtorder/2)*2  # Filter order must be even

    # Passband edge to cutoff (transition band center; -6 dB)
    dfArray = [[df, [-df, df]], [-df, [df, -df]]]
    cutoffArray = edgeArray+np.array(dfArray[revfilt][len(edgeArray)-1])/2
    print('pop_eegfiltnew() - cutoff frequency(ies) (-6 dB): '
          + str(cutoffArray) + ' Hz\n')

    # Window
    winArray = signal.hamming(int(filtorder)+1)
    # Filter coefficients
    if revfilt == 1:
        filterTypeArray = ['high', 'stop']
        b = firws(filtorder, cutoffArray/fNyquist, winArray,
                  filterTypeArray[len(edgeArray)-1])
    else:
        b = firws(filtorder, cutoffArray/fNyquist, winArray)

    return filtorder, b
