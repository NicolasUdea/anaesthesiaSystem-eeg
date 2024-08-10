# -*- coding: utf-8 -*-
"""
Created on Wed May  4 13:22:29 2022

@author: Maria Camila Villa, Yeimmy Morales
@reviewer: Nicolas Vargas Flores
"""
from PyQt5.QtWidgets import QApplication
from controller import Controller
from model.model import Model
from view import View
import model.read_openbci
import sys


class Main:
    """
    Initialize the QT application and assign the model and the view.
    """
    def __init__(self):
        self._app = QApplication(sys.argv)
        self._view = View()
        openbci = model.read_openbci.OpenBCI()
        self._system = Model(openbci)
        self._controller = Controller(self._view, self._system)
        self._view.set_controller(self._controller)

    def main(self):
        """
        Initialize the system.
        """
        self._view.show()
        sys.exit(self._app.exec_())


if __name__ == "__main__":
    main_instance = Main()
    main_instance.main()
