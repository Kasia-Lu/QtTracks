# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 12:21:10 2019

@author: Katarzyna Luszczak
"""

from Plot_Window import Plot_Window

class Histogram(Plot_Window):
    def __init__(self, data_in, ax_in=None):
        super().__init__()
        
        self.ax = ax_in or self.figure.add_subplot(111)
        self.data = data_in
        self.color_pt = 'black'
        self.plot()
    
    def plot(self):
        self.ax.hist(self.data['Length'], bins=20, range=(0,21), edgecolor='black', linewidth=1.0, normed=1, cumulative=0)
        self.ax.set_title('Track length distributrion - measured tracks')
        self.ax.set_xlabel('Track length (μm)')
        self.ax.set_ylabel('Frequency')
        self.ax.set_xlim(0, 20)
        self.ax.set_xticks(range(21))