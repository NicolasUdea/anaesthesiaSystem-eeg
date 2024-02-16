"""Example program to demonstrate how to send a multi-channel time series to
LSL."""
import time
from random import random as rand
from PyQt5.QtWidgets import QFileDialog, QApplication, QMessageBox


from pylsl import StreamInfo, StreamOutlet

class RandData(object):
    # first create a new stream info (here we set the name to BioSemi,
    # the content-type to EEG, 8 channels, 100 Hz, and float-valued data) The
    # last value would be the serial number of the device or some other more or
    # less locally unique identifier for the stream as far as available (you
    # could also omit it but interrupted connections wouldn't auto-recover)
    def __init__(self):
        self.info = StreamInfo('BioSemi', 'EEG', 8, 250, 'float32', 'myuid34234')
    
        # next make an outlet
        self.outlet = StreamOutlet(self.info)
    
    print("now sending data...")
    def sample(self):
        app = QApplication([])
        file_path, _ = QFileDialog.getOpenFileName(None, "Select an EEG file", "Si", "Text Files(*.txt)")


        if file_path != "":
            with open(file_path, "r") as file:
                dataset = file.readlines()

            for sample in dataset:
                if sample[0] != "%":
                    # Separate the string into a list and select only the eeg data converted into float
                    self.mysample = [float(x.strip()) for x in sample.split(",")[1:9]]

                    # make a new random 8-channel sample; this is converted into a
                    # pylsl.vectorf (the data type that is expected by push_sample)
                    #self.mysample = [rand()*50, rand()*50, rand()*50, rand()*50, rand()*50, rand()*50, rand()*50, rand()*50]

                    # now send it and wait for a bit
                    self.outlet.push_sample(self.mysample)

                    print(self.mysample)
                    time.sleep(0.01)
                            
                    
                else:
                    pass
            
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setInformativeText("All data has been read successfully")
            msg.setWindowTitle("Read finished")
            msg.exec_()


        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Error")
            msg.setInformativeText("No file selected")
            msg.setWindowTitle("Error")
            msg.exec_()

        

            

            

if __name__ == '__main__':
    data = RandData()
    data.sample();


