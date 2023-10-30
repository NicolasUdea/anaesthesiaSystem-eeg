# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 21:33:36 2020

@author: Maria Camila Villa, Yeimmy Morales
"""

import numpy as np
from pylsl import StreamInlet
from pylsl import resolve_stream
import csv


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
        samples, timestamp = self.__inlet.pull_chunk()
        samples = np.transpose(np.asanyarray(samples))
        
        #print(samples.shape)

        # try:
        #     # perform the ohm-law operation.
        #     # V = received rms voltage. i = device current = 6 nA
        #     for i in range(0, 3):
        #         Z_i = ((samples[i])*np.sqrt(2))/(6*pow(10, -9))
        #         self.Z.append(Z_i/1000)
        #         # print("impedancia: " + str(Z_i))
        # except:
        #     pass

        if (samples is None) or  (timestamp is None):
            return
        # path ='C:/Users/Usuario/Desktop/Nuevos registros/EEG/prueba.txt'
        # with open(path, 'w', encoding='UTF8', newline='') as f:
        #     writer = csv.writer(f, delimiter=',')
        #     writer.writerow(samples)
        try:
            print(samples.shape[1])
            self.__data = np.roll(self.__data, samples.shape[1])

            # BIS
            # Fp1-Fpz
            self.__data[0, 0:samples.shape[1]] = samples[2, :]-samples[1, :]
            # Fp2-Fpz
            self.__data[1, 0:samples.shape[1]] = samples[3, :]-samples[1, :]

            #print(self.__data.shape)
            # path ='C:/Users/Usuario/Desktop/Nuevos registros/EEG/prueba.txt'
            
            # with open(path, 'w', encoding='UTF8', newline='') as f:
            #     writer = csv.writer(f, delimiter=',')
            #     writer.writerow(samples.shape[1])


        except IndexError:
            print("Error making the montages")
            pass        

        return self.__data[0, :].copy(), self.__data[1, :].copy()
