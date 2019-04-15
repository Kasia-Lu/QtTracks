# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 16:25:17 2019

@author: Katarzyna Luszczak
"""
from seaborn import kdeplot

from Plot_Window import Plot_Window

#------------------------------------------------------------------------------
class KDE_plot(Plot_Window):
    def __init__(self, data_in, ax_in=None):
        super().__init__()
        
        self.ax = ax_in or self.figure.add_subplot(111)
        self.data = data_in
        self.color_pt = 'black'
        self.plot()
        
    def plot(self):
        kdeplot(self.data['Age'], shade=True, ax=self.ax)
        self.x_label_text = 'Age (Ma)'
        self.y_label_text = 'Probability'
        self.title_text = 'KDE plot'
        self.ax.set_xlabel(self.x_label_text)
        self.ax.set_ylabel(self.y_label_text)
        self.ax.set_title(self.title_text)