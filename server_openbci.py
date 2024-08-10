# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 15:18:37 2019

This module handles the data streaming from the OpenBCI Cyton board to LSL (Lab Streaming Layer).

Author: user
"""

import numpy as np
import csv
from pyOpenBCI import OpenBCICyton
from pylsl import StreamInfo, StreamOutlet
from serial.tools import list_ports

SERIAL_OPENBCI = 'DQ0081'


class DataServer:
    """
    DataServer class to handle the streaming of EEG data from OpenBCI to LSL.
    """

    def __init__(self):
        self._scale_factor_eeg = 4500000 / 24 / (2**23 - 1)  # uV/count
        self._info_eeg = StreamInfo('OpenBCIEEG', 'EEG', 8, 250, 'float32', 'OpenBCItestEEG')
        self._outlet_eeg = StreamOutlet(self._info_eeg)

    def lsl_streamers(self, sample):
        """
        Stream EEG data to LSL and save to a CSV file.

        Args:
            sample: The sample data from OpenBCI.
        """
        data = np.array(sample.channels_data) * self._scale_factor_eeg
        self._outlet_eeg.push_sample(data)

        # Save data to a CSV file
        path = r"C:\Users\ahoga\OneDrive\Escritorio\Anestesia\prueba.txt"
        try:
            with open(path, 'a', encoding='UTF8', newline='') as f:
                writer = csv.writer(f, delimiter=',')
                writer.writerow(data)
        except IOError as e:
            print(f"Error writing to file: {e}")


def main():
    """
    Main function to initialize the OpenBCI board and start streaming data.
    """
    lista_puertos = list_ports.comports()
    print(lista_puertos)
    for serial_device in lista_puertos:
        code_serial = serial_device.serial_number
        if code_serial and code_serial.startswith(SERIAL_OPENBCI):
            board = OpenBCICyton(port=serial_device.device, daisy=False)
            data_server = DataServer()
            board.start_stream(data_server.lsl_streamers)
            return

    print('No OpenBCI device found. Please connect and restart the program.')
    input('Press Enter to exit...')


if __name__ == "__main__":
    main()
