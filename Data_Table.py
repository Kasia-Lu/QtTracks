# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 11:13:25 2019

@author: Katarzyna Luszczak
"""
import csv
import os

from PyQt5.QtWidgets import (QTableWidget,
                             QTableWidgetItem, 
                             QFileDialog)

#------------------------------------------------------------------------------
class Data_Table(QTableWidget):
    def __init__(self, data_type, r=40, c=7):
        super().__init__(r, c)
        self.data_type = data_type
        
        if self.data_type == 'LA':
            col_headers = ['Ns', 'Area', 'U/Ca', '1σ U/Ca', 'DPar']
        elif self.data_type == 'EDM':
            col_headers = ['Ns', 'Ni', 'Area', 'DPar']
        elif self.data_type == 'lengths':
            col_headers = ['Length', 'Angle', 'DPar']
            
        self.setHorizontalHeaderLabels(col_headers)
        self.open_sheet()
        
        self.show()
        
    def open_sheet(self):
        path = QFileDialog.getOpenFileName(self, 'Open CSV', os.getenv('HOME'), 'CSV(*.csv)')
        
        if path[0] != '':
            with open(path[0], newline='') as csv_file:
                self.setRowCount(0)
                self.setColumnCount(10)
                
                my_file = csv.reader(csv_file, delimiter=';', quotechar='|')
                
                for row_data in my_file:
                    row = self.rowCount()
                    self.insertRow(row)
                    
                    if len(row_data) > 10:
                        self.setColumnCount(len(row_data))
                        
                    for column, stuff in enumerate(row_data):
                        item = QTableWidgetItem(stuff)
                        self.setItem(row, column, item)  