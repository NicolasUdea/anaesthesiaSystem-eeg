# -*- coding: utf-8 -*-
"""
Created on Tue May  3 09:04:26 2022

@author: Maria Camila Villa,Yeimmy Morales
"""
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
import numpy as np
import pyqtgraph as pg
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as fig_canvas

'''
En el archivo view.py se genera la interfaz gráfica
---
Se define la clase View, que hereda de QMainWindow. 
Esta clase representa la ventana principal de la aplicación.
'''

class View(QMainWindow):
    def __init__(self, ppal=None):
        """
        View class constructor, loads a ui file.

        Returns
        -------
        None.

        """
        super().__init__(ppal)
        loadUi('as_monitoring.ui', self)
        self.setup()

    def setup(self):
        """
        Connect the start and stop buttons, generate the images
        and configure the color map for the scalogram plotting.

        Returns
        -------
        None.

        """
        self.start_botton.clicked.connect(self.start_signal)
        self.stop_botton.clicked.connect(self.stop_signal)
        self.start_botton2.clicked.connect(self.start_signal)
        self.stop_botton2.clicked.connect(self.stop_signal)
        
        # Scales option 
        self.scales.addItem("50 uV")
        self.scales.addItem("100 uV")
        self.scales.addItem("200 uV")
        self.scales.addItem("400 uV")
        self.scales.addItem("1000 uV")
        self.scales.addItem("10000 uV")

        self.scales_2.addItem("50 uV")
        self.scales_2.addItem("100 uV")
        self.scales_2.addItem("200 uV")
        self.scales_2.addItem("400 uV")
        self.scales_2.addItem("1000 uV")
        self.scales_2.addItem("10000 uV")
        
        # Images generation
        self.img = pg.ImageItem()
        self.img2 = pg.ImageItem()
        
        

        ticks = [(0, '0'), (100, '10'), (200, '20'), (300, '30')]
        ay_f4 = self.f4_fz_spectogram.getAxis('left')
        ay_f4.setTicks([ticks])
        ay_f3 = self.f3_fz_spectogram.getAxis('left')
        ay_f3.setTicks([ticks])

        self.f4_fz_spectogram.clear()
        self.f3_fz_spectogram.clear()

        self.figure = plt.figure()
        self.canvas = fig_canvas(self.figure)
        self.f4_fz_spectogram.addItem(self.img)
        self.f3_fz_spectogram.addItem(self.img2)
        self.f4_fz_spectogram.repaint()
        self.f3_fz_spectogram.repaint()

        # Colormap for the scalogram
        pos = np.arange(0, 1, 0.0625)
        self.color = np.array([[0, 0, 127, 150], [0, 0, 255, 150],
                                [0, 191, 255, 150], [0, 255, 255, 150],                  
                                [0, 255, 120, 150], [0, 255, 0, 150],
                                [127, 255, 0, 150], [205, 255, 0, 150],    
                                [255, 255, 0, 150], [255, 200, 0, 150],
                                [255, 108, 0, 150], [255, 62, 0, 150],
                                [255, 0, 0, 150], [220, 0, 0, 150],
                                [178, 0, 0, 150], [127, 0, 0, 150]], dtype=np.ubyte)

        cmap = pg.ColorMap(pos, self.color)
        lut = cmap.getLookupTable(0, 1, 255)
        self.img.setLookupTable(lut)
        self.img.setLevels([-50, 40])
        self.img2.setLookupTable(lut)
        self.img2.setLevels([-50, 40])
        self.f4_fz_spectogram.setLabel('left', 'Frequency', units='Hz')
        self.f3_fz_spectogram.setLabel('left', 'Frequency', units='Hz')
        self.f4_fz_spectogram.hideAxis('bottom')
        self.f3_fz_spectogram.hideAxis('bottom')

    def graph_data(self, data):
        """
        Generate EEG plot by hemispheres.

        Parameters
        ----------
        data : ndarray
        Array with EEG values ​​for both, right and left hemispheres.

        Returns
        -------
        None.

        """
        f3_fz = data[0]
        f4_fz = data[1]
        time_eeg = np.arange(0, 5, 0.004)

        # Basic tab
        self.eeg_graphr2.clear()
        self.eeg_graphl2.clear()
        # f4_fz
        self.eeg_graphr2.plot(time_eeg, f4_fz, pen=('#C7C7C7'), enableAutoRange=False)
        self.eeg_graphr2.setLabel('bottom', 'Time', units='s')
        if (self.scales_2.currentIndex()==0):
            self.eeg_graphr2.setYRange(-50, 50)
        if (self.scales_2.currentIndex()==1):
            self.eeg_graphr2.setYRange(-100, 100)
        if (self.scales_2.currentIndex()==2):
            self.eeg_graphr2.setYRange(-200, 200)
        if (self.scales_2.currentIndex()==3):
            self.eeg_graphr2.setYRange(-400, 400)
        if (self.scales_2.currentIndex()==4):
            self.eeg_graphr2.setYRange(-1000, 1000)
        if (self.scales_2.currentIndex()==5):
            self.eeg_graphr2.setYRange(-10000, 10000)
        self.eeg_graphr2.repaint()

        # f3_fz
        self.eeg_graphl2.plot(time_eeg, f3_fz, pen=('#C7C7C7'))
        self.eeg_graphl2.setLabel('bottom', 'Time', units='s')
        if (self.scales_2.currentIndex()==0):
            self.eeg_graphl2.setYRange(-50, 50)
        if (self.scales_2.currentIndex()==1):
            self.eeg_graphl2.setYRange(-100, 100)
        if (self.scales_2.currentIndex()==2):
            self.eeg_graphl2.setYRange(-200, 200)
        if (self.scales_2.currentIndex()==3):
            self.eeg_graphl2.setYRange(-400, 400)
        if (self.scales_2.currentIndex()==4):
            self.eeg_graphl2.setYRange(-1000, 1000)
        if (self.scales_2.currentIndex()==5):
            self.eeg_graphl2.setYRange(-10000, 10000)
        self.eeg_graphl2.repaint()

        # Advanced tab
        self.eeg_graphr.clear()
        self.eeg_graphl.clear()
        # f4_fz
        self.eeg_graphr.plot(time_eeg, f4_fz, pen=('#C7C7C7'))
        self.eeg_graphr.setLabel('bottom', 'Time', units='s')
        if (self.scales.currentIndex()==0):
            self.eeg_graphr.setYRange(-50, 50)
        if (self.scales.currentIndex()==1):
            self.eeg_graphr.setYRange(-100, 100)
        if (self.scales.currentIndex()==2):
            self.eeg_graphr.setYRange(-200, 200)
        if (self.scales.currentIndex()==3):
            self.eeg_graphr.setYRange(-400, 400)
        if (self.scales.currentIndex()==4):
            self.eeg_graphr.setYRange(-1000, 1000)
        if (self.scales.currentIndex()==5):
            self.eeg_graphr.setYRange(-10000, 10000)
        self.eeg_graphr.repaint()

        # f3_fz
        self.eeg_graphl.plot(time_eeg, f3_fz, pen=('#C7C7C7'))
        self.eeg_graphl.setLabel('bottom', 'Time', units='s')
        if (self.scales.currentIndex()==0):
            self.eeg_graphl.setYRange(-50, 50)
        if (self.scales.currentIndex()==1):
            self.eeg_graphl.setYRange(-100, 100)
        if (self.scales.currentIndex()==2):
            self.eeg_graphl.setYRange(-200, 200)
        if (self.scales.currentIndex()==3):
            self.eeg_graphl.setYRange(-400, 400)
        if (self.scales.currentIndex()==4):
            self.eeg_graphl.setYRange(-1000, 1000)
        if (self.scales.currentIndex()==5):
            self.eeg_graphl.setYRange(-10000, 10000)
        self.eeg_graphl.repaint()

    def graph_spectra(self, data):
        """
        Generate EEG power spectrum plot by hemispheres.

        Parameters
        ----------
        data : ndarray
            Array with power and frequency values for left hemisphere.
        data1 : ndarray
            Array with power and frequency values for right hemisphere.

        Returns
        -------
        None.

        """
        power_f3 = data[0]
        power_f4 = data[1]
        
        
        self.img.setImage((power_f4.T)*10)
        self.img2.setImage((power_f3.T)*10)

    def graph_asym(self, data):
        """
        Generates a graph that represents the asymmetry between hemispheres.

        Parameters
        ----------
        data : ndarray
        Array with asymmetry values.

        Returns
        -------
        None.

        """
        asym = data
        #self.asym_graph.clear()
        #self.asym_graph.plot(np.abs(asym*100), pen=('w'))
        #self.asym_graph.repaint()
        #self.asym_graph.setLabel('left', 'Asymmetry')
        #self.asym_graph.hideAxis('bottom')
        #self.asym_graph.setYRange(0, 100)

        self.asym_lcd.display(abs(asym*100))
        self.asym_lcd.repaint()

    #def graph_lpe(self, data):
        #
        #Displays the Lumped permutation entropy by hemispheres.

        #Parameters
        #----------
        #data : ndarray
        #    Array with lumped permutation entropy values by hemispheres.

        #Returns
        #-------
        #None.

        
        #pe_f3 = data[0]
        #pe_f4 = data[1]
        #self.f3_lcd.display('{:.02f}'.format(pe_f3))
        #self.f4_lcd.display('{:.02f}'.format(pe_f4))
        #self.f3_lcd.repaint()
        #self.f4_lcd.repaint()

    def light_graph(self, data):
        powers_f3 = data[0]
        powers_f4 = data[1]
        
        print(powers_f3)
        print(powers_f4)

        theta_f3 = np.mean(powers_f3[0])
        alpha_f3 = np.mean(powers_f3[1])
        beta_f3 = np.mean(powers_f3[2])
        # gamma_f3 = np.mean(powers_f3[3])

        theta_f4 = np.mean(powers_f4[0])
        alpha_f4 = np.mean(powers_f4[1])
        beta_f4 = np.mean(powers_f4[2])
        # gamma_f4 = np.mean(powers_f4[3])

        self.alpha_lcdl.display(alpha_f3)
        self.alpha_lcdl2.display(alpha_f3)
        self.alpha_lcdr.display(alpha_f4)
        self.alpha_lcdr2.display(alpha_f4)
        
        if alpha_f3 > beta_f3:
            self.alpha_lightl.setStyleSheet('background-color: #4FA600;'
                                            'border-radius: 25px;'
                                            'border: 2px solid white')
            #self.alpha_lcdl.display('8-13')
            self.alpha_lightl2.setStyleSheet('background-color: #4FA600;'
                                             'border-radius: 25px;'
                                             'border: 2px solid white')
            #self.alpha_lcdl2.display('8-13')
        else:
            self.alpha_lightl.setStyleSheet('background-color: red;'
                                            'border-radius: 25px;'
                                            'border: 2px solid white')
            #self.alpha_lcdl.display('13-30')
            self.alpha_lightl2.setStyleSheet('background-color: red;'
                                             'border-radius: 25px;'
                                             'border: 2px solid white')
            #self.alpha_lcdl2.display('13-30')

        if alpha_f4 > beta_f4:
            self.alpha_lightr.setStyleSheet('background-color: #4FA600;'
                                            'border-radius: 25px;'
                                            'border: 2px solid white')
            #self.alpha_lcdr.display('8-13')
            self.alpha_lightr2.setStyleSheet('background-color: #4FA600;'
                                             'border-radius: 25px;'
                                             'border: 2px solid white')
            #self.alpha_lcdr2.display('8-13')
        else:
            self.alpha_lightr.setStyleSheet('background-color: red;'
                                            'border-radius: 25px;'
                                            'border: 2px solid white')
            #self.alpha_lcdr.display('13-30')
            self.alpha_lightr2.setStyleSheet('background-color: red;'
                                             'border-radius: 25px;'
                                             'border: 2px solid white')
            #self.alpha_lcdr2.display('13-30')

    def bar_graph(self, data):
        powers_f3 = data[0]
        powers_f4 = data[1]

        # Left hemisphere
        theta_f3 = np.mean(np.abs(powers_f3[0]))
        alpha_f3 = np.mean(np.abs(powers_f3[1]))
        beta_f3 = np.mean(np.abs(powers_f3[2]))
        gamma_f3 = np.mean(np.abs(powers_f3[3]))

        # Right hemisphere
        theta_f4 = np.mean(np.abs(powers_f4[0]))
        alpha_f4 = np.mean(np.abs(powers_f4[1]))
        beta_f4 = np.mean(np.abs(powers_f4[2]))
        gamma_f4 = np.mean(np.abs(powers_f4[3]))

        powers_f3 = [theta_f3, alpha_f3, beta_f3, gamma_f3]
        powers_f4 = [theta_f4, alpha_f4, beta_f4, gamma_f4]
        x = np.arange(4)

        names = ['Theta', 'Alpha', 'Beta', 'Gamma']
        ticks = list(enumerate(names))

        b1 = pg.BarGraphItem(x=x, height=powers_f3, width=0.5, brush='#0833A2')
        b2 = pg.BarGraphItem(x=x, height=powers_f4, width=0.5, brush='#0833A2')
        self.rhythmsl.setBackground([0, 0, 0, 0])  # Background color
        self.rhythmsl.clear()
        self.rhythmsl.addItem(b1)

        self.rhythmsl.setLimits(xMax=4.5)
        self.rhythmsl.hideAxis('left')
        ax = self.rhythmsl.getAxis('bottom')
        ax.setTicks([ticks])
        self.rhythmsl.repaint()

        self.rhythmsr.setBackground([0, 0, 0, 0])  # Background color
        self.rhythmsr.clear()
        self.rhythmsr.addItem(b2)

        self.rhythmsr.setLimits(xMax=4.5)
        self.rhythmsr.hideAxis('left')
        ax2 = self.rhythmsr.getAxis('bottom')
        ax2.setTicks([ticks])
        self.rhythmsr.repaint()

    def start_signal(self):
        """
        Calls the thread fuction using the controller.

        Returns
        -------
        None.

        """
        self.__controller.start()

    def stop_signal(self):
        """
        Calls the stop function of the model using the controller.

        Returns
        -------
        None.

        """
        self.__controller.stop()

    def set_controller(self, c):
        """
        Set the controller in the view.

        Parameters
        ----------
        c : Class
            Class controller.

        Returns
        -------
        None.

        """
        self.__controller = c

    def closeEvent(self, event):
        print('Inside Close Event')
        self.__controller.finish_thread()
        event.accept()
