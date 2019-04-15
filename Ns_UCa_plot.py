# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 16:25:17 2019

@author: Katarzyna Luszczak
"""
from Plot_Window import Plot_Window

#------------------------------------------------------------------------------
class Ns_UCa_plot(Plot_Window):
    def __init__(self, data_in, ax_in=None):
        super().__init__()

        self.ax = ax_in or self.figure.add_subplot(111)
        self.data = data_in
        self.color_pt = 'black'
        self.plot()
        
    def plot(self):
        self.ax.clear()
        self.ax.scatter(x=self.data['Ns'], y=self.data['U/Ca'], s=30, c=self.color_pt)
        self.x_label_text = 'Ns'
        self.y_label_text = 'U/Ca'
        self.title_text = 'Ns vs. U/Ca plot'
        self.ax.set_xlabel(self.x_label_text)
        self.ax.set_ylabel(self.y_label_text)
        self.ax.set_title(self.title_text)