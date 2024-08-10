# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 21:33:36 2020

@author: Maria Camila Villa, Yeimmy Morales
"""

import numpy as np
from pylsl import StreamInlet
from pylsl import resolve_stream


class OpenBCI(object):
    def __init__(self):
        """
        Resolve an EEG stream on the lab network.

        Returns
        -------
        None.

        """
        self.__fs = 250
        self.__channels = 2
        self.__data = np.zeros((self.__channels, 1250))  # 5 seconds
        self.__streams_EEG = resolve_stream('type', 'EEG')

    def start_data(self):
        """
        Create a new inlet to read from the stream info.

        Returns
        -------
        None.

        """
        self.__inlet = StreamInlet(self.__streams_EEG[0], max_buflen=1250)
        self.__inlet.pull_chunk()

    def stop_data(self):
        """
        Close the inlet to stop reading from the stream info.

        Returns
        -------
        None.

        """
        self.__inlet.close_stream()

    def read_data(self):
        """
        Get a new sample of the EEG signal.

        Returns
        -------
        ndarray
            F3_Fz montage.
        ndarray
            F4_fz montage.

        """
        self.Z = []
        samples, _ = self.__inlet.pull_chunk()
        
        samples = np.transpose(np.asanyarray(samples))

        if (samples is None) :
            return
        
        try:

            self.__data = np.roll(self.__data, samples.shape[1])

            self.__data[:self.__channels,:samples.shape[1]] = samples[:self.__channels, :]
            

        except IndexError:
            print("Error making the montages")
            pass        

        return self.__data
