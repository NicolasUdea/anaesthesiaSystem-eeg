
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 15:18:37 2019

@author: user
"""

from pyOpenBCI import OpenBCICyton
from pylsl import StreamInfo, StreamOutlet

import numpy as np
from serial.tools import list_ports
import csv

serial_openBCI = 'DQ0081';

class DataServer(object):

    def __init__(self):
        self.SCALE_FACTOR_EEG = (4500000)/24/(2**23-1) #uV/count
        self.info_eeg = StreamInfo('OpenBCIEEG', 'EEG', 8, 250, 'float32', 'OpenBCItestEEG')
        self.outlet_eeg = StreamOutlet(self.info_eeg)
        
    def lsl_streamers(self,sample):
        data = np.array(sample.channels_data)*self.SCALE_FACTOR_EEG
        self.outlet_eeg.push_sample(data)
      #'C:/Users/Usuario/Desktop/Registros/valeria.txt'    
        try:
            path ='C:/Users/Usuario/Desktop/Registros/rosa_Anestesia.txt'
            
            with open(path, 'a', encoding='UTF8', newline='') as f:
                writer = csv.writer(f, delimiter=',')
                writer.writerow(data)
        except:
            pass 
    
Lista_puertos = list_ports.comports();
print (Lista_puertos)
for serial_device in Lista_puertos:
    code_serial = serial_device.serial_number 
    if code_serial != None:
        if code_serial.startswith(serial_openBCI):
    
            board = OpenBCICyton(port=serial_device.device, daisy=False)
            Data = DataServer()
    
            board.start_stream(Data.lsl_streamers)
            Data.read_data()
            print('')

print('No hay dispositivo OpenBCI, conectar y volver a iniciar el programa')
input('Presione enter para finalizar ...')
