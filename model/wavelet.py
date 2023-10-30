# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 09:22:07 2022

@author: Maria Camila Villa,Yeimmy Morales
"""

import pywt
import numpy as np


def thr_hard(coeff, thr, s):
    """
    Hard thresholding

    Parameters
    ----------
    coeff : list
        Ordered list of coefficients arrays.The first element is the
        aproximation coefficients array and the following elements are details
        coefficients arrays.
    thr : ndarray
        Thresholds for filtering.
    s :  ndarray
        Multiple weighting.

    Returns
    -------
    y : list
        Hard thresholding.

    """
    y = list()
    if type(s) == np.ndarray:
        for i in range(0, len(coeff)):
            y.append(np.multiply(coeff[i], np.abs(coeff[i]) >= (thr*s[i])))
    else:
        for i in range(0, len(coeff)):
            y.append(np.multiply(coeff[i], np.abs(coeff[i]) >= (thr*s)))
    return y


def thr_universal(coeff):
    """
    Universal threshold

    Parameters
    ----------
    coeff : list
        Ordered list of coefficients arrays.The first element is the
        aproximation coefficients array and the following elements are details
        coefficients arrays.

    Returns
    -------
    thr : ndarray
        Universal threshold for filtering.

    """

    num_samples = 0
    for i in range(0, len(coeff)):
        num_samples = num_samples+coeff[i].shape[0]
    # umbral universal
    thr = np.sqrt(2*(np.log(num_samples)))
    return thr


def multiple_ln(coeff):
    """
    Multiple weighting

    Parameters
    ----------
    coeff : list
        Ordered list of coefficients arrays.The first element is the
        aproximation coefficients array and the following elements are details
        coefficients arrays.

    Returns
    -------
    stdc : array
        Multiple weighting array.

    """
    stdc = np.zeros((len(coeff), 1))
    for i in range(1, len(coeff)):
        stdc[i] = (np.median(np.absolute(coeff[i])))/0.6745
    return stdc


def wavelet(data):
    """
    Wavelet filtering

    Parameters
    ----------
    data : ndarray
        Time series.

    Returns
    -------
    x_filt : ndarray
        Time serie filtered by Wavelet.

    """
    ll = int(np.floor(np.log2(data.shape[0])))
    coeff = pywt.wavedec(data, 'db6', level=ll)
    thr = thr_universal(coeff)
    s = multiple_ln(coeff)
    coeff_t = thr_hard(coeff, thr, s)
    # Signal reconstruction
    x_rec = pywt.waverec(coeff_t, 'db6')
    x_rec = x_rec[0:data.shape[0]]
    x_filt = np.squeeze(data-x_rec)
    return x_filt
