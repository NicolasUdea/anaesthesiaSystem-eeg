"""Example program to demonstrate how to send a multi-channel time series to LSL."""
import time
from PyQt5.QtWidgets import QFileDialog, QApplication, QMessageBox
from pylsl import StreamInfo, StreamOutlet


class RandData:
    """
    RandData class to handle the generation and streaming of random EEG data to LSL.
    """

    def __init__(self):
        self._info = StreamInfo('BioSemi', 'EEG', 8, 250, 'float32', 'myuid34234')
        self._outlet = StreamOutlet(self._info)

    def sample(self):
        """
        Stream EEG data from a selected file to LSL.

        This method opens a file dialog to select an EEG file, reads the data,
        and streams it to LSL.
        """
        # Create a QApplication instance, which is required for any PyQt application.
        # The empty list is passed to avoid passing any command-line arguments.
        app = QApplication([])
        file_path, _ = QFileDialog.getOpenFileName(None, "Select an EEG file", "", "Text Files(*.txt)")

        if file_path:
            try:
                with open(file_path, "r") as file:
                    dataset = file.readlines()

                for sample in dataset:
                    if sample[0] != "%":
                        # Separate the string into a list and select only the EEG data converted into float
                        mysample = [float(x.strip()) for x in sample.split(",")[1:9]]
                        self._outlet.push_sample(mysample)
                        print(mysample)
                        time.sleep(0.01)

                self._show_message("Read finished", "All data has been read successfully", QMessageBox.Information)
            except IOError as e:
                self._show_message("Error", f"Error reading file: {e}", QMessageBox.Critical)
        else:
            self._show_message("Error", "No file selected", QMessageBox.Warning)

    @staticmethod
    def _show_message(title, text, icon):
        """
        Display a message box.

        Args:
            title (str): The title of the message box.
            text (str): The text of the message box.
            icon (QMessageBox.Icon): The icon of the message box.
        """
        msg = QMessageBox()
        msg.setIcon(icon)
        msg.setText(text)
        msg.setWindowTitle(title)
        msg.exec_()


if __name__ == '__main__':
    data = RandData()
    data.sample()
