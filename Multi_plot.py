# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 16:55:22 2019

@author: Katarzyna Luszczak
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import (QLabel,
                             QGridLayout,
                             QPushButton,
                             QDialog,
                             QCheckBox,
                             QButtonGroup,
                             QAbstractButton)

from Plot_Window import Plot_Window

from Ns_UCa_plot import Ns_UCa_plot
from Age_DPar_plot import Age_DPar_plot
from Radial_plot import Radial_plot
from KDE_plot import KDE_plot

#------------------------------------------------------------------------------
class Multi_plot(Plot_Window):
    def __init__(self, data_in, ax_in=None):
        super().__init__()
        
        self.ax = ax_in or self.figure.add_subplot(111)
        self.data = data_in
        
        self.options()
        
    def options(self):    
        self.d = QDialog()
        self.d.setWindowTitle('Choose plot types for the multi plot...')
        
        layout = QGridLayout()
        
        self.plot_types = QButtonGroup()
        self.plot_types.setExclusive(False)
        self.plot1 = QCheckBox('Ns vs. U/Ca plot')
        self.plot2 = QCheckBox('Age vs. DPar')
        self.plot3 = QCheckBox('KDE plot')
        self.plot4 = QCheckBox('Radial plot')
        self.plot5 = QCheckBox('Measured track lengths historgram')
        self.plot6 = QCheckBox('Projected track lengths historgram')
        
        self.plot_types.addButton(self.plot1)
        self.plot_types.addButton(self.plot2)
        self.plot_types.addButton(self.plot3)
        self.plot_types.addButton(self.plot4)
        self.plot_types.addButton(self.plot5)
        self.plot_types.addButton(self.plot6)
        
        self.plot_types.buttonClicked['QAbstractButton *'].connect(self.button_clicked)
        self.plot_types.buttonClicked['int'].connect(self.button_clicked)
                
        self.ok_btn = QPushButton('OK')
        
        layout.addWidget(QLabel('Choose plot types'), 0, 0)
        layout.addWidget(self.plot1, 1, 0)
        layout.addWidget(self.plot2, 2, 0)
        layout.addWidget(self.plot3, 3, 0)
        layout.addWidget(self.plot4, 4, 0)
        layout.addWidget(self.plot5, 5, 0)
        layout.addWidget(self.plot6, 6, 0)
        layout.addWidget(self.ok_btn, 7, 0, 1, 2)
        self.d.setLayout(layout)
        self.ok_btn.clicked.connect(self.draw_plots)        
        self.d.exec()

    def draw_plots(self):
        self.ax1 = self.figure.add_subplot(2, 2, 1)
        self.ax2 = self.figure.add_subplot(2, 2, 2)
        self.ax3 = self.figure.add_subplot(2, 2, 3)
        self.ax4 = self.figure.add_subplot(2, 2, 4)
        Ns_UCa_plot(data_in=self.data, ax_in=self.ax1)
        Age_DPar_plot(data_in=self.data, ax_in=self.ax2)
        KDE_plot(data_in=self.data, ax_in=self.ax3)
        Radial_plot(data_in=self.data, ax_in=self.ax4, sample_name=None)
    
    # button_clicked slot
    @pyqtSlot(QAbstractButton)
    @pyqtSlot(int)
    def button_clicked(self, button_or_id):
        if isinstance(button_or_id, QAbstractButton):
            dictionary = {
                    'Ns vs. U/Ca plot': 'Ns_UCa_plot(x)',
                    'Age vs. DPar': 'Age_DPar_plot(x)',
                    'KDE plot': 'KDE_plot(x)',
                    'Radial plot': 'Radial_plot(x)'
                    }
            for key, value in dictionary.items():
                if "'{}' was clicked".format(button_or_id.text()) == key:
                    print(dictionary[key])