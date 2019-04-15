# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 11:11:20 2019

@author: Katarzyna Luszczak
"""

import pandas as pd
import numpy as np

from PyQt5.QtWidgets import (QVBoxLayout,
                             QHBoxLayout,
                             QWidget,
                             QLabel,
                             QLineEdit,
                             QGridLayout,
                             QPushButton,
                             QGroupBox,
                             QSizePolicy,
                             QTableWidgetItem)

from Data_Table import Data_Table

#------------------------------------------------------------------------------
class Age_Data_Window(QWidget):
    def __init__(self, data_type, plots_menu_items):
        super().__init__()
        
        self.data_type = data_type
        self.input_side_grid()
        grid_main = QHBoxLayout()
        grid_table = QVBoxLayout()
        grid_side = QVBoxLayout()
        grid_main.addLayout(grid_table)
        grid_main.addLayout(grid_side)
        grid_side.addWidget(self.grid_calc)
        
        self.table = Data_Table(data_type=data_type)
        grid_table.addWidget(self.table)
        
        self.setLayout(grid_main)
        
        self.menu_Ns_Ni_plot = plots_menu_items[0]
        self.menu_radial_plot = plots_menu_items[4]
        self.menu_Ns_UCa_plot = plots_menu_items[1]
        self.menu_KDE_plot = plots_menu_items[3]
        self.menu_age_DPar_plot = plots_menu_items[2]
        self.menu_multi_plot = plots_menu_items[5]
        
        self.show()
        
    def input_side_grid(self):
        self.grid_calc = QGroupBox('Calculate AFT ages')
        layout = QGridLayout()
        
        calc_btn = QPushButton('Calculate')
        self.zeta_input = QLineEdit()
        self.zeta_1s_input = QLineEdit()
        self.c_age = QLineEdit()
        self.c_age.setEnabled(False)
        self.c_age_1s = QLineEdit()
        self.c_age_1s.setEnabled(False)
        self.p_age = QLineEdit()
        self.p_age.setEnabled(False)
        self.p_age_1s = QLineEdit()
        self.p_age_1s.setEnabled(False)
        
        sizePolicy = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Fixed)
        
        if self.data_type == 'LA':
                       
            layout.addWidget(QLabel('Zeta:'), 0, 0)
            layout.addWidget(self.zeta_input, 0, 1)
            layout.addWidget(QLabel('+/-'), 0, 2)
            layout.addWidget(self.zeta_1s_input, 0, 3)
            layout.addWidget(calc_btn, 1, 0)
            layout.addWidget(QLabel('Central age:'), 2, 0)
            layout.addWidget(self.c_age, 2, 1)
            layout.addWidget(QLabel('+/-'), 2, 2)
            layout.addWidget(self.c_age_1s, 2, 3)
            layout.addWidget(QLabel('Ma'), 2, 4)
            layout.addWidget(QLabel('Pooled age:'), 3, 0)
            layout.addWidget(self.p_age, 3, 1)
            layout.addWidget(QLabel('+/-'), 3, 2)
            layout.addWidget(self.p_age_1s, 3, 3)
            layout.addWidget(QLabel('Ma'), 3, 4)
            
            calc_btn.clicked.connect(self.calculate_ages_LA)
            
        elif self.data_type == 'EDM':
            
            self.rhod_input = QLineEdit()
            self.Nd_input = QLineEdit()
            
            layout.addWidget(QLabel('Zeta'), 0, 0)
            layout.addWidget(self.zeta_input, 0, 1)
            layout.addWidget(QLabel('+/-'), 0, 2)
            layout.addWidget(self.zeta_1s_input, 0, 3)
            layout.addWidget(QLabel('Rho_D'), 1, 0)
            layout.addWidget(self.rhod_input, 1, 1)
            layout.addWidget(QLabel('Nd:'), 1, 2)
            layout.addWidget(self.Nd_input, 1, 3)
            layout.addWidget(calc_btn, 2, 0)
            layout.addWidget(QLabel('Central age:'), 3, 0)
            layout.addWidget(self.c_age, 3, 1)
            layout.addWidget(QLabel('+/-'), 3, 2)
            layout.addWidget(self.c_age_1s, 3, 3)
            layout.addWidget(QLabel('Ma'), 3, 4)
            layout.addWidget(QLabel('Pooled age:'), 4, 0)
            layout.addWidget(self.p_age, 4, 1)
            layout.addWidget(QLabel('+/-'), 4, 2)
            layout.addWidget(self.p_age_1s, 4, 3)
            layout.addWidget(QLabel('Ma'), 4, 4)
            
            self.rhod_input.setSizePolicy(sizePolicy)
            self.rhod_input.setMinimumWidth(40)
            self.Nd_input.setSizePolicy(sizePolicy)
            self.Nd_input.setMinimumWidth(30)
            
            calc_btn.clicked.connect(self.calculate_ages_EDM)

        self.zeta_input.setSizePolicy(sizePolicy)
        self.zeta_input.setMinimumWidth(40)
        self.zeta_1s_input.setSizePolicy(sizePolicy)
        self.zeta_1s_input.setMinimumWidth(30)
        self.c_age.setSizePolicy(sizePolicy)
        self.c_age.setMinimumWidth(40)
        self.c_age_1s.setSizePolicy(sizePolicy)
        self.c_age_1s.setMinimumWidth(30)
        self.p_age.setSizePolicy(sizePolicy)
        self.p_age.setMinimumWidth(40)
        self.p_age_1s.setSizePolicy(sizePolicy)
        self.p_age_1s.setMinimumWidth(30)

        layout.setColumnMinimumWidth(0, 20)
        layout.setColumnMinimumWidth(1, 40)
        layout.setColumnMinimumWidth(2, 10)
        layout.setColumnMinimumWidth(3, 30)
        layout.setColumnMinimumWidth(4, 10)
        layout.setHorizontalSpacing(5)
        
        self.grid_calc.setLayout(layout)
    
    def calculate_ages_LA(self):
        zeta = float(self.zeta_input.text())
        zeta_1s = float(self.zeta_1s_input.text())
        
        lambda_d = 1.55E-10
        g = 0.5
        
        Ns = []
        A = []
        ratio = []
        ratio_1s = []
        DPar = []
        for r in range(50):
            if self.table.item(r, 0) is not None:
                Ns_i = int(self.table.item(r, 0).text())
                A_i = float(self.table.item(r, 1).text())
                ratio_i = float(self.table.item(r, 2).text())
                ratio_1s_i = float(self.table.item(r, 3).text())
                DPar_i = float(self.table.item(r, 4).text())
                Ns.append(Ns_i)
                A.append(A_i)
                ratio.append(ratio_i)
                ratio_1s.append(ratio_1s_i)
                DPar.append(DPar_i)
                
        age_data = pd.DataFrame({
                'Ns': Ns,
                'A': A,
                'U/Ca': ratio,
                '1s U/Ca': ratio_1s,
                'DPar': DPar
                })

        age_i = round(((1 / 1000000) * (1 / lambda_d) * np.log(1 + lambda_d * zeta * g * (age_data['Ns'] / (age_data['A'] * age_data['U/Ca'])))), 2)
        sigma_i = ((1 / age_data['Ns']) + ((age_data['1s U/Ca'] / age_data['U/Ca']) ** 2) + ((zeta_1s / zeta) ** 2) ) ** 0.5
        age_1s_i = round((sigma_i * age_i), 2)
        
        age_data['Age'] = age_i
        age_data['SE'] = age_1s_i
        
        z = age_data['Age'].apply(np.log)
        sigma_z = age_data['SE'] / age_data['Age']
        
        central_value = ((z / sigma_z ** 2).sum()) / ((1 / sigma_z ** 2).sum())
        central_age = round((np.exp(central_value)) ,1)
        
        pooled_age = round(((1 / 1000000) * (1 / lambda_d) * np.log(1 + lambda_d * zeta * g * (age_data['Ns'].sum() / (age_data['A'] * age_data['U/Ca']).sum()))), 1)
        pooled_sigma = 1/age_data['Ns'].sum() + (age_data['1s U/Ca'] ** 2 * age_data['A'] ** 2).sum() / ((age_data['U/Ca'] * age_data['A']).sum() ** 2) + (zeta_1s/zeta ** 2) ** 0.5
        pooled_age_SE = round((pooled_sigma * pooled_age), 1)
        
        self.c_age.setText(str(central_age))
        self.c_age.setEnabled(True)
        self.c_age_1s.setText('xx')
        self.p_age.setText(str(pooled_age))
        self.p_age.setEnabled(True)
        self.p_age_1s.setText(str(pooled_age_SE))
        self.p_age_1s.setEnabled(True)
            
        col_headers_update = ['Ns', 'Area', 'U/Ca', '1σ U/Ca', 'DPar', 'Age', 'Age SE']
        self.table.setHorizontalHeaderLabels(col_headers_update)
        
        for index, age in enumerate(age_i):
            SE = age_1s_i[index]
            self.table.setItem(index, 5, QTableWidgetItem(str(age)))
            self.table.setItem(index, 6, QTableWidgetItem(str(SE)))
            
        self.menu_radial_plot.setEnabled(True)  
        self.menu_Ns_UCa_plot.setEnabled(True)
        self.menu_KDE_plot.setEnabled(True)
        self.menu_age_DPar_plot.setEnabled(True)
        self.menu_multi_plot.setEnabled(True)
        
        self.a_data = age_data
        return self.a_data
    
    def calculate_ages_EDM(self):
        zeta = float(self.zeta_input.text())
        zeta_1s = float(self.zeta_1s_input.text())
        rhod = float(self.rhod_input.text())
        Nd = float(self.Nd_input.text())
        
        lambda_d = 1.55E-10
        g = 0.5
        
        Ns = []
        Ni = []
        A = []
        DPar = []
        for r in range(30):
            if self.table.item(r, 0) is not None:
                Ns_i = int(self.table.item(r, 0).text())
                Ni_i = int(self.table.item(r, 1).text())
                A_i = float(self.table.item(r, 2).text())
                DPar_i = float(self.table.item(r, 3).text())
                Ns.append(Ns_i)
                Ni.append(Ni_i)
                A.append(A_i)
                DPar.append(DPar_i)
                
        age_data = pd.DataFrame({
                'Ns': Ns,
                'Ni': Ni,
                'A': A,
                'DPar': DPar
                })

        age_i = round(((1 / 1000000) * (1 / lambda_d) * np.log(1 + ((lambda_d * zeta * g * (age_data['Ns'] / age_data['A']) * rhod) / (age_data['Ni'] / age_data['A']) ))), 2)
        age_1s_i = round(((1 / age_data['Ns'] + 1 / age_data['Ni'] + 1 / Nd + (zeta_1s/zeta) ** 2 ) ** 0.5) * age_i, 2)
        
        age_data['Age'] = age_i
        age_data['SE'] = age_1s_i
        
        z = age_data['Age'].apply(np.log)
        sigma_z = age_data['SE'] / age_data['Age']
        
        central_value = (z / sigma_z ** 2).sum() / (1 / sigma_z ** 2).sum()
        central_age = round((np.exp(central_value)), 2)
        
        pooled_age = round(((1 / 1000000) * (1 / lambda_d) * np.log(1 + ((lambda_d * zeta * g * (age_data['Ns'].sum() / age_data['A'].sum()) * rhod) / (age_data['Ni'].sum() / age_data['A'].sum()) ))), 2)
        
        self.c_age.setText(str(central_age))
        self.c_age.setEnabled(True)
        self.c_age_1s.setText('xx')
        #self.c_age_1s.setEnabled(True)
        self.p_age.setText(str(pooled_age))
        self.p_age.setEnabled(True)
        self.p_age_1s.setText('xx')
        #self.p_age_1s.setEnabled(True)
            
        col_headers_update = ['Ns', 'Ni', 'Area', 'DPar', 'Age', 'Age SE']
        self.table.setHorizontalHeaderLabels(col_headers_update)
        
        for index, age in enumerate(age_i):
            SE = age_1s_i[index]
            self.table.setItem(index, 4, QTableWidgetItem(str(age)))
            self.table.setItem(index, 5, QTableWidgetItem(str(SE)))
            
        self.menu_radial_plot.setEnabled(True)  
        self.menu_Ns_Ni_plot.setEnabled(True)
        self.menu_KDE_plot.setEnabled(True)
        self.menu_age_DPar_plot.setEnabled(True)
        self.menu_multi_plot.setEnabled(True)

        self.a_data = age_data
        self.zeta = zeta
        self.zeta_1s = zeta_1s
        self.rhod = rhod
        self.Nd = Nd