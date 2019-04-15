# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 15:14:02 2019

@author: Katarzyna Luszczak
"""

import numpy as np
import matplotlib.pyplot as plt

from Plot_Window import Plot_Window

#------------------------------------------------------------------------------
class Radial_plot(Plot_Window):
    def __init__(self, data_in, sample_name, ax_in=None):
        super().__init__()

        self.ax = ax_in or self.figure.add_subplot(111)
        self.data = data_in
        self.sample_name = sample_name
        self.color_pt = 'black'
        age, unc, comp, comp_type = self.load_data()
        self.draw_radial_plot(age, unc, comp, comp_type)
        self.figure = plt.figure(figsize=(10, 5), dpi=100)
        plt.rcParams.update({'font.size': 10})
        plt.show()
        
    def load_data(self):

        if (self.data.columns[1] == 'A'):
            age = self.data.iloc[:,5]
            unc = self.data.iloc[:,6]
            comp = self.data.iloc[:,4]
            comp_type = self.data.columns[4]
                
        elif (self.data.columns[1] == 'Ni'):
            Ns = self.data.iloc[:,0]
            Ni = self.data.iloc[:,1]
            A = self.data.iloc[:,2]
            comp = self.data.iloc[:,3]
            comp_type = self.data.columns[3]
            
            lambd = 1.55125E-10      # radioactive decay rate of 238U in 1/yr
            c = 0.5
            rho_d = 800000
            Nd = 6000
            zeta = 313
            zeta_se = 10
            
            age = round(((1 / 1000000) * (1/lambd) * np.log(1 + (lambd * zeta * c * (Ns / A) * rho_d) / (Ni / A))), 2)
            unc = age * ((1 / Ns) + (1 / Ni) + (1 / Nd) + (zeta_se / zeta) ** 2) ** 0.5
        
        return age, unc, comp, comp_type
    
    def draw_radial_plot(self, age, unc, comp, comp_type):
        
        x_corr, y_corr, central_value, central_age = self.xy_coordinates(age, unc)
        radial_plot = self.ax.scatter(x_corr, y_corr, c=comp, s=50, cmap='autumn_r', edgecolor='black')
        
        x_max = self.axes_setup(self.ax, x_corr)
        self.add_colorbar(radial_plot, comp_type)
        ticks_span = self.arc_ticks_span(age)
        R = self.draw_arc(radial_plot, self.ax, x_max, age, ticks_span, central_value)
        self.draw_central_age_line(R)
        self.add_text_labels(central_age)
        
    def xy_coordinates(self, age, unc):  
        z = age.apply(np.log)       # using logarthmic transformation (after Vermeesch, 2008)
        sigma_z = unc / age
        central_value = (z / sigma_z ** 2).sum() / (1 /sigma_z ** 2).sum()
        central_age = np.exp(central_value)
        
        x_corr = 1 / sigma_z
        y_corr = (z - central_value) / sigma_z
    
        return x_corr, y_corr, central_value, central_age
        
    def arc_ticks_span(self, age):
        age_diff = round((max(age) + 5), -1) - round((min(age) + 5), -1)
        
        if age_diff > 100:
            ticks_span = 50
        elif age_diff > 50:
            ticks_span = 20
        elif age_diff <= 50:
            ticks_span = 10
            
        return ticks_span
    
    def axes_setup(self, ax, x_corr):
        x_max = round(max(x_corr) + 0.5)       
        ax.set_xlim(0, x_max + 2)
        ax.set_ylim(-6, 6)
        
        ax.set_xlabel('precision (t/$\sigma$)')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_position(('data', -6))
        ax.spines['bottom'].set_bounds(0, x_max + 1) 
        ax.spines['left'].set_bounds(-2, 2)
        ax.set_xticks(np.arange(0, x_max + 2, 1))
        ax.set_yticks([-2, -1, 0, 1, 2])
        
        ax2 = ax.twiny()
        ax2.set_xlabel('% relative error', labelpad=-30)
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        ax2.spines['bottom'].set_position(('data', -5.9))
        ax2.spines['bottom'].set_bounds(0, x_max + 1)
        ax2.spines['left'].set_bounds(-2, 2)
        ax2.xaxis.set_ticks_position('bottom')
        ax2.xaxis.set_label_position('bottom')
        
        x_ticks = np.arange(2, x_max + 2, 1)
        ax2.set_xticks(x_ticks)
        ax2.set_xticklabels((100 / x_ticks).astype(int))
        ax2.set_xlim(ax.get_xlim())
        ax2.tick_params(direction='in', pad=-15)
        
        return x_max
    
    def add_colorbar(self, plot, comp_type):
        plt.colorbar(plot, orientation='horizontal', aspect=40, pad=0.15, label=comp_type)

    def z_axis_arc(self, points, radius, central_value, h):
            x_arc = radius / (1 + h**2 * ((points - central_value) ** 2)) ** 0.5
            y_arc = (points - central_value) * x_arc
            
            return x_arc, y_arc
    
    def arc_ticks_and_labels(self, tick_ages, x_t, y_t, x_t2, y_t2, ax): 
        for i, value in enumerate(tick_ages):
            x_1 = x_t[i]
            y_1 = y_t[i]
            x_2 = x_t2[i]
            y_2 = y_t2[i]
            plt.plot([x_1, x_2], [y_1, y_2], c='black')
            plt.annotate(value, (x_t2[i] + 0.1, y_t2[i] - 0.1), transform=ax.transAxes)
        
    def draw_arc(self, plot, ax, x_max, age, ticks_span, central_value):
        R = x_max + 1
        R2 = R + 0.1
        h = (ax.get_xlim()[1] - ax.get_xlim()[0]) / (ax.get_ylim()[1] - ax.get_ylim()[0])
        
        tick_ages_0 = np.arange((round((min(age) + 5), -1)), (round(max(age), -1)), ticks_span)
        tick_ages = np.append(tick_ages_0, ([round(min(age), 1), round(max(age), 1)]))
        ticks = np.log(tick_ages)
        
        arc_point_ages = np.arange(min(age),max(age),0.5)
        arc_points = np.log(arc_point_ages)
            
        x_t, y_t = self.z_axis_arc(ticks, R, central_value, h)
        x_t2, y_t2 = self.z_axis_arc(ticks, R2, central_value, h)
        x_arc, y_arc = self.z_axis_arc(arc_points, R, central_value, h)
            
        plt.plot(x_arc, y_arc, c='black', linewidth=1.0)
        self.arc_ticks_and_labels(tick_ages, x_t, y_t, x_t2, y_t2, ax)
        
        return R
        
    def draw_central_age_line(self, R):    
        plt.plot([0,R], [0,0], linestyle=':', c='gray')
        
    def add_text_labels(self, central_age):    
        plt.text(0, 6.0, self.sample_name, fontsize=11)
        plt.text(0, 5.0, ('Central age: ' + str(round((central_age), 2)) + ' Ma'), fontsize=10)
        