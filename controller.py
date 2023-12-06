
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QThread


class Controller(object):
    # Signals to communicate between objects
    eeg_data = pyqtSignal(object)
    spectra_data = pyqtSignal(object)
    asym_data = pyqtSignal(object)
    lpe_data = pyqtSignal(object)
    light_data = pyqtSignal(object)
    bar_data = pyqtSignal(object)

    def __init__(self, view, model):
        """
        Assign the model and the view.

        Generate a worker thread and connect the signals and slots.
        The thread is made for the model class. Connects the model data
        to the view.

        Parameters
        ----------
        view : class
            View class.
        model : class
            Model class.

        Returns
        -------
        None.

        """
        self.__model = model
        self.__view = view

        # Create a QThread object
        self.thread = QThread()

        # Create a worker object
        self.worker = self.__model

        # Move worker to the thread
        # You can use worker objects by moving them to the thread
        self.worker.moveToThread(self.thread)

        # When the Start signal is emit, begins execution of the thread
        # by calling run()
        self.thread.started.connect(self.worker.run)

        # Tells the thread's event loop to exit
        self.worker.finished.connect(self.thread.quit)

        # To delete the worker and the thread objects when the work is done
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        # Connect signals with slots. A slot is a Python callable
        self.worker.eeg_data.connect(self.__view.graph_data)
        self.worker.spectra_data.connect(self.__view.graph_spectra)
        self.worker.asym_data.connect(self.__view.graph_asym)
        #self.worker.lpe_data.connect(self.__view.graph_lpe)
        self.worker.light_data.connect(self.__view.light_graph)
        self.worker.bar_data.connect(self.__view.bar_graph)

    def worker_thread(self):
        """
        Starts the worker thread.

        Returns
        -------
        None.

        """
        # Start the thread
        self.thread.start()

    def start(self):
        """
        Calls the start function of the model and the worker_thead function
        of the controller.

        Returns
        -------
        None.

        """
        self.__model.start()
        self.worker_thread()

    def stop(self):
        """
        Calls the stop function of the model.

        Returns
        -------
        None.

        """
        self.__model.stop()
        print('Stop Data')

    def finish_thread(self):
        """
        Calls the finish_thread function of the model and stop the worker.
        Also exits the thread and wait until it actually exit.

        Returns
        -------
        None.

        """
        if self.thread.isRunning() is True:
            print("Stop worker thread")
            self.__model.finish_thread()
            self.worker.stop()
            self.thread.exit()
            self.thread.wait()
        else:
            print("Worker thread is not running")
