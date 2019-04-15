# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 14:15:38 2019

@author: Katarzyna Luszczak
"""

from Plot_Window import Plot_Window

class Age_DPar_plot(Plot_Window):
    def __init__(self, data_in, ax_in=None):
        super().__init__()

        self.ax = ax_in or self.figure.add_subplot(111)
        self.data = data_in
        self.color_pt = 'black'
        self.plot()
        
    def plot(self):
        self.ax.clear()
        self.ax.scatter(x=self.data['Age'], y=self.data['DPar'], s=30, c=self.color_pt)
        self.x_label_text = 'Age (Ma)'
        self.y_label_text = 'DPar (μm)'
        self.title_text = 'Age vs. DPar plot'
        self.ax.set_xlabel(self.x_label_text)
        self.ax.set_ylabel(self.y_label_text)
        self.ax.set_title(self.title_text)