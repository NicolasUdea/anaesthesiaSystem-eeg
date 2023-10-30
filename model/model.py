# -*- coding: utf-8 -*-
"""
Created on Mon May  2 09:17:08 2022

@author: Maria Camila Villa,Yeimmy Morales
"""
import numpy as np
from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal
import scipy.signal as signal
from model.filters import filter_design
import model.read_openbci
from model.wavelet import wavelet
from model.relative_powers import relative_powers
from model.scalogram import scalogram
#from model.espect import spect as scalogram
from model.lumped_entropy import lumped_permutation_entropy
openbci = model.read_openbci.OpenBCI()
import time


class Model(QObject):
    # Signals to communicate between objects
    finished = pyqtSignal()
    eeg_data = pyqtSignal(object)
    spectra_data = pyqtSignal(object)
    asym_data = pyqtSignal(object)
    lpe_data = pyqtSignal(object)
    light_data = pyqtSignal(object)
    bar_data = pyqtSignal(object)

    def __init__(self):
        """
        filters are designed and start data inlet.

        Returns
        -------
        None.

        """
        super().__init__()
        self.execute_thread = True
        self.continue_count = False
        self.__fs = 250  # sample frecuency
        print("looking for an EEG stream...")

        # designed filters
        order, self.highpass = filter_design(self.__fs, locutoff=4,
                                             hicutoff=0, revfilt=1)
        order, self.lowpass = filter_design(self.__fs, locutoff=0,
                                            hicutoff=25, revfilt=0)

    def run(self):
        """
        Read the data and do all the processing.

        Returns
        -------
        None.

        """
        while self.execute_thread is True:
            while self.continue_count:
                # Takes the data and generate the montages
                f3, f4 = openbci.read_data()

                # Calls the filtering function
                self.f3_fz = self.filtering(f3)
                self.f4_fz = self.filtering(f4)

                # Compute the continuous wavelet transform to generate the
                # scalogram
                power_f4 = scalogram(self.f4_fz)
                power_f3 = scalogram(self.f3_fz)

                # Power spectrum of EEG signal is calculated
                total_power_f3, powers_f3, = relative_powers(self.f3_fz)
                total_power_f4, powers_f4, = relative_powers(self.f4_fz)

                # Asymmetry
                subtract_power = total_power_f3-total_power_f4
                add_power = total_power_f3+total_power_f4
                asym = subtract_power/add_power
                
                print(abs(asym*100))

                # Compute the lumped permutation entropy
                #pe_f3 = lumped_permutation_entropy(self.f3_fz)
                #pe_f4 = lumped_permutation_entropy(self.f4_fz)

                # Send the signals created
                self.eeg_data.emit(np.array([self.f3_fz, self.f4_fz]))
                self.spectra_data.emit(np.array([power_f3, power_f4]))
                self.asym_data.emit(asym)
                #self.lpe_data.emit(np.array([pe_f3, pe_f4]))
                self.light_data.emit(np.array([powers_f3, powers_f4]))
                #self.light_data.emit(np.array([f3, f4]))
                self.bar_data.emit(np.array([powers_f3, powers_f4]))
                time.sleep(0.2)

        # emit the finished signal when the loop is done
        self.finished.emit()
        print('finished')

    def start(self):
        """
        Start data inlet.

        Returns
        -------
        None.

        """
        # provide a bool run condition for the class
        self.continue_count = True
        openbci.start_data()

    def stop(self):
        """
        Stops data inlet.

        Returns
        -------
        None.

        """
        self.continue_count = False
        openbci.stop_data()

    def finish_thread(self):
        """
        Change the flag to stop the thread.

        Returns
        -------
        None.

        """
        print('finishing')
        self.execute_thread = False

    def filtering(self, data):
        """
        Apply linear filters and wavelet filter.

        Parameters
        ----------
        data : ndarray
            Array of data to be filtered.

        Returns
        -------
        data_filtered : ndarray
            The filtered data.

        """
        # apply the linear filters
        data_hp = signal.filtfilt(self.highpass, 1, data)
        data_lp = signal.filtfilt(self.lowpass, 1, data_hp)

        # Aplly the Wavelet filter
        #data_filtered = wavelet(data_lp)
        return data_lp
