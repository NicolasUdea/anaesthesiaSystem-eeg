# -*- coding: utf-8 -*-
"""
Created on Mon May  2 09:17:08 2022

@author: Maria Camila Villa,Yeimmy Morales
"""


import numpy as np
import time
from scipy.signal import filtfilt
from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal

from model.filters import filter_design
from model.relative_powers import relative_powers
from model.scalogram import scalogram





class Model(QObject):
    # Signals to communicate between objects
    
    '''
    Clase definida como el back de la interfaz, creacion de variables de 
    interes.
    '''
    finished = pyqtSignal()
    eeg_data = pyqtSignal(object)
    spectra_data = pyqtSignal(object)
    asym_data = pyqtSignal(object)
    lpe_data = pyqtSignal(object)
    light_data = pyqtSignal(object)
    bar_data = pyqtSignal(object)

    def __init__(self,openbci):
        
        """
        filters are designed and start data inlet. lineal filters designed
        as follow:
            
            lowpass = cutfreq = 4 Hz
            Highpass = cutfreq = 25 Hz

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
        _, self.highpass = filter_design(self.__fs, locutoff=4,
                                             hicutoff=0, revfilt=1)
        _, self.lowpass = filter_design(self.__fs, locutoff=0,
                                            hicutoff=25, revfilt=0)
        self.__openbci = openbci


    def run(self):
        """
        Read the data and do all the processing.

        Returns
        -------
        None.

        """
        while self.execute_thread is True:
            while self.continue_count:
                
                #timpo inicial en segundo ti
                
                # Takes the data and generate the montages
                self.__electrodes_data = self.__openbci.read_data()

                # Calls the filtering function
                self.filtered_electrodes = self.filtering(self.__electrodes_data)
                

                # Compute the continuous wavelet transform to generate the
                # scalogram
                power = scalogram(self.filtered_electrodes)
                

                # Power spectrum of EEG signal is calculated
                total_power, powers = relative_powers(self.filtered_electrodes)

                # Asymmetry
                subtract_power = total_power[0]-total_power[1]
                add_power = total_power[0]+total_power[1]
                asym = subtract_power/add_power


                # Send the signals created
                self.eeg_data.emit(np.array(self.filtered_electrodes))
                self.spectra_data.emit(np.array(power))
                self.asym_data.emit(asym)
                self.light_data.emit(np.array(powers))
                self.bar_data.emit(np.array(powers))
                
                #timpo final en segundo tf
                
                # 1 - (tf - ti)
                time.sleep(1)

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
        self.__openbci.start_data()

    def stop(self):
        """
        Stops data inlet.

        Returns
        -------
        None.

        """
        self.continue_count = False
        self.__openbci.stop_data()

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
        data_hp = filtfilt(self.highpass, 1, data, axis=1)
        data_lp = filtfilt(self.lowpass, 1, data_hp, axis=1)

        # Aplly the Wavelet filter
        #data_filtered = wavelet(data_lp)
        data_filtered = data_lp
        return data_filtered
