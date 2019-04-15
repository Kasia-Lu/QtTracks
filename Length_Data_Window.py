# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 11:11:20 2019

@author: Katarzyna Luszczak
"""

import pandas as pd

from PyQt5.QtWidgets import (QVBoxLayout,
                             QHBoxLayout,
                             QWidget,
                             QLabel,
                             QLineEdit,
                             QGridLayout,
                             QPushButton,
                             QGroupBox,
                             QSizePolicy,
                             QComboBox)

from Data_Table import Data_Table

#------------------------------------------------------------------------------
class Length_Data_Window(QWidget):
    def __init__(self, plots_menu_items=None):
        super().__init__()
        
        self.input_side_grid()
        grid_main = QHBoxLayout()
        grid_table = QVBoxLayout()
        grid_side = QVBoxLayout()
        grid_main.addLayout(grid_table)
        grid_main.addLayout(grid_side)
        grid_side.addWidget(self.grid_calc)
        
        self.table = Data_Table(data_type='lengths')
        grid_table.addWidget(self.table)

        self.setLayout(grid_main)
        
        self.add_measured_lengths()
        
        self.menu_hist_m_plot = plots_menu_items[6]
        self.menu_hist_p_plot = plots_menu_items[7]
        self.menu_hist_m_plot.setEnabled(True)

        
    def input_side_grid(self):
        self.grid_calc = QGroupBox('Calculate MTL and project track lengths')
        layout = QGridLayout()
        
        self.calc_btn = QPushButton('Calculate')
        self.combo_box_etch = QComboBox()
        self.combo_box_etch.addItem('5.0 M')
        self.combo_box_etch.addItem('5.5 M')
        self.combo_box_proj = QComboBox()
        self.combo_box_proj.addItem('None')
        self.combo_box_proj.addItem('Donelick et al., 1999')
        self.combo_box_proj.addItem('Ketcham et al., 2007')
        self.mtl_m = QLineEdit()
        self.mtl_m.setEnabled(False)
        self.mtl_m_1s = QLineEdit()
        self.mtl_m_1s.setEnabled(False)
        self.mtl_p = QLineEdit()
        self.mtl_p.setEnabled(False)
        self.mtl_p_1s = QLineEdit()
        self.mtl_p_1s.setEnabled(False)
         
        layout.addWidget(QLabel('Etchant:'), 0, 0)
        layout.addWidget(self.combo_box_etch, 0, 1, 1, 4)
        layout.addWidget(QLabel('Projection model:'), 1, 0)
        layout.addWidget(self.combo_box_proj, 1, 1, 1, 4)
        layout.addWidget(QLabel('Measured MTL:'), 2, 0)
        layout.addWidget(self.mtl_m, 2, 1)
        layout.addWidget(QLabel('+/-'), 2, 2)
        layout.addWidget(self.mtl_m_1s, 2, 3)
        layout.addWidget(QLabel('μm'), 2, 4)
        layout.addWidget(QLabel('Projected MTL:'), 3, 0)
        layout.addWidget(self.mtl_p, 3, 1)
        layout.addWidget(QLabel('+/-'), 3, 2)
        layout.addWidget(self.mtl_p_1s, 3, 3)
        layout.addWidget(QLabel('μm'), 3, 4)
        layout.addWidget(self.calc_btn, 4, 0)
        
        sizePolicy = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Fixed)
        
        self.combo_box_etch.setSizePolicy(sizePolicy)
        self.combo_box_etch.setMinimumWidth(80)
        self.combo_box_proj.setSizePolicy(sizePolicy)
        self.combo_box_proj.setMinimumWidth(80)
        self.mtl_m.setSizePolicy(sizePolicy)
        self.mtl_m.setMinimumWidth(40)
        self.mtl_m_1s.setSizePolicy(sizePolicy)
        self.mtl_m_1s.setMinimumWidth(30)
        self.mtl_p.setSizePolicy(sizePolicy)
        self.mtl_p.setMinimumWidth(40)
        self.mtl_p_1s.setSizePolicy(sizePolicy)
        self.mtl_p_1s.setMinimumWidth(30)
        
        layout.setColumnMinimumWidth(0, 20)
        layout.setColumnMinimumWidth(1, 42)
        layout.setColumnMinimumWidth(2, 12)
        layout.setColumnMinimumWidth(3, 33)
        layout.setColumnMinimumWidth(4, 12)
        layout.setHorizontalSpacing(5)
        
        self.calc_btn.clicked.connect(self.calculate_lengths)
        
        self.grid_calc.setLayout(layout)
     
    def add_measured_lengths(self):
        
        Length = []
        Angle = []
        DPar = []
        
        for r in range(150):
            if self.table.item(r,0) is None:
                break
            else:
                Length_i = float(self.table.item(r, 0).text())
                Angle_i = float(self.table.item(r, 1).text())
                DPar_i = float(self.table.item(r, 2).text())
                Length.append(Length_i)
                Angle.append(Angle_i)
                DPar.append(DPar_i)
                
        self.length_data = pd.DataFrame({
                'Length': Length,
                'Angle': Angle,
                'DPar': DPar
                })
 
        self.show()
        
        self.l_data = self.length_data
        return self.l_data
    
    def calculate_lengths(self):        
        MTLm = round(self.length_data['Length'].mean(), 2)
        MTLm_1s = round(self.length_data['Length'].std(), 2)
        
        self.mtl_m.setText(str(MTLm))
        self.mtl_m.setEnabled(True)
        self.mtl_m_1s.setText(str(MTLm_1s))
        self.mtl_m_1s.setEnabled(True)
                 
        #col_headers_update = ['Length', 'Angle', 'DPar', 'Length projected']
        #self.table.setHorizontalHeaderLabels(col_headers_update)
        
        #self.menu_hist_p_plot.setEnabled(True)