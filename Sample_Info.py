# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 16:39:26 2019

@author: Katarzyna Luszczak
"""

from PyQt5.QtWidgets import (QWidget,
                             QLabel,
                             QLineEdit,
                             QGroupBox,
                             QGridLayout,
                             QVBoxLayout,
                             QPushButton)


class Sample_Info(QWidget):
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout()
        self.infobox = QGroupBox('Input sample information...')
        grid_layout = QGridLayout()
        
        self.sample_name_le = QLineEdit()
        self.long_le = QLineEdit()
        self.lat_le = QLineEdit()
        self.elevation_le = QLineEdit()
        self.depth_le = QLineEdit()
        self.lithology_le = QLineEdit()
        self.stratigraphy_le = QLineEdit()
        self.save_btn = QPushButton('Save')
        self.save_btn.clicked.connect(self.get_inserted_text)

        
        grid_layout.addWidget(QLabel('Sample name:'), 0, 0)
        grid_layout.addWidget(self.sample_name_le, 0, 1)
        grid_layout.addWidget(QLabel('X / Long:'), 1, 0)
        grid_layout.addWidget(self.long_le, 1, 1)
        grid_layout.addWidget(QLabel('Y / Lat:'), 2, 0)
        grid_layout.addWidget(self.lat_le, 2, 1)
        grid_layout.addWidget(QLabel('Elevation'), 3, 0)
        grid_layout.addWidget(self.elevation_le, 3, 1)
        grid_layout.addWidget(QLabel('Depth:'), 4, 0)
        grid_layout.addWidget(self.depth_le, 4, 1)
        grid_layout.addWidget(QLabel('Lithology:'), 5, 0)
        grid_layout.addWidget(self.lithology_le, 5, 1)
        grid_layout.addWidget(QLabel('Stratigraphy:'), 6, 0)
        grid_layout.addWidget(self.stratigraphy_le, 6, 1)
        grid_layout.addWidget(self.save_btn,8,0)       
        grid_layout.setSpacing(15)
        
        self.infobox.setLayout(grid_layout)
        
        layout.addWidget(self.infobox)
        layout.addStretch()

        self.setLayout(layout)
        
        self.show
        
    def get_inserted_text(self):
        self.sample_name = self.sample_name_le.text()
        self.long = self.long_le.text()
        self.lat = self.lat_le.text()
        self.elevation = self.elevation_le.text()
        self.depth = self.depth_le.text()
        self.lithology = self.lithology_le.text()
        self.stratigraphy = self.stratigraphy_le.text()
        
        