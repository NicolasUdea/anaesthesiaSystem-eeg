# -*- coding: utf-8 -*-
"""
Created on Wed May  4 13:22:29 2022

@author: Maria Camila Villa, Yeimmy Morales
"""
import sys
from PyQt5.QtWidgets import QApplication
from model.model import Model
from view import View
from controller import Controller


class Main(object):
    def __init__(self):
        """
        To initialize the QT application and assign the model and the view.

        Returns
        -------
        None.

        """
        self.__app = QApplication(sys.argv)
        self.__view = View()
        self.__system = Model()
        self.__controller = Controller(self.__view, self.__system)
        self.__view.set_controller(self.__controller)

    def main(self):
        """
        To initialize the system.

        Returns
        -------
        None.

        """
        self.__view.show()
        sys.exit(self.__app.exec_())


M = Main()
M.main()
