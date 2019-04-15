# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 12:01:30 2019

@author: Katarzyna Luszczak
"""

import matplotlib.pyplot as plt

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QWidget,
                             QLabel,
                             QLineEdit,
                             QGridLayout,
                             QPushButton,
                             QAction,
                             QColorDialog,
                             QToolBar,
                             QDialog,
                             QVBoxLayout)

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

#------------------------------------------------------------------------------
class Plot_Window(QWidget):
    def __init__(self):
        super().__init__()
        
        Act_Save = QAction(QIcon('icons/icon_save.png'), 'Save', self)
        Act_Save.triggered.connect(self.save_image)
        Act_Color = QAction(QIcon('icons/icon_colors.png'), 'Colors', self)
        Act_Color.triggered.connect(self.color_picker)
        Act_Axes = QAction(QIcon('icons/icon_axes.png'), 'Change axes', self)
        Act_Axes.triggered.connect(self.change_axes)
        
        my_toolbar = QToolBar()
        my_toolbar.addAction(Act_Color)
        my_toolbar.addAction(Act_Axes)
        my_toolbar.addAction(Act_Save)

        self.figure = plt.figure(figsize=(5, 5), dpi=100)
        self.canvas = FigureCanvas(self.figure)

        self.toolbar = my_toolbar

        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addStretch()
        self.setLayout(layout)
        
    def color_picker(self):
        self.color = QColorDialog.getColor()
        self.color_pt = str(self.color.name())        
        self.plot()
        self.canvas.draw()
        
    def save_image(self):
        plt.savefig('figures/KDE_plot.png')
        
    def change_axes(self):
        self.d = QDialog()
        self.d.setWindowTitle('Set Axes Limits...')
        
        layout = QGridLayout() 
        self.title = QLineEdit()
        self.x_label = QLineEdit()
        self.y_label = QLineEdit()
        self.x1_le = QLineEdit()
        self.x2_le = QLineEdit()
        self.y1_le = QLineEdit()
        self.y2_le = QLineEdit()
        self.x_tick = QLineEdit()
        self.y_tick = QLineEdit()
        self.ok_btn = QPushButton('OK')
        
        #default values, read from the default plot, to be shown in line edits
        self.x1_le.setText(str(round(self.ax.get_xlim()[0])))
        self.x2_le.setText(str(round(self.ax.get_xlim()[1])))
        self.y1_le.setText(str(self.ax.get_ylim()[0]))
        self.y2_le.setText(str(self.ax.get_ylim()[1]))
        self.x_label.setText(self.x_label_text)
        self.y_label.setText(self.y_label_text)
        self.title.setText(self.title_text)
        
        layout.addWidget(QLabel('Title:'), 0, 0)
        layout.addWidget(self.title, 0, 1, 1, 2)
        layout.addWidget(QLabel('X-axis label:'), 1, 0)
        layout.addWidget(self.x_label, 1, 1, 1, 2)
        layout.addWidget(QLabel('Y-axis label:'), 2, 0)
        layout.addWidget(self.y_label,2,1,1,3)
        layout.addWidget(QLabel('Set axes limits:'), 3, 0, 1, 3)
        layout.addWidget(QLabel('X:'), 4, 0)
        layout.addWidget(self.x1_le, 4, 1)
        layout.addWidget(self.x2_le, 4, 2)
        layout.addWidget(QLabel('Y:'), 5, 0)
        layout.addWidget(self.y1_le, 5, 1)
        layout.addWidget(self.y2_le, 5, 2)
        layout.addWidget(QLabel('Set axes ticks values:'), 6, 0, 1, 3)
        layout.addWidget(QLabel('X:'), 7, 0)
        layout.addWidget(QLabel('every'), 7, 1)
        layout.addWidget(self.x_tick, 7, 2)
        layout.addWidget(QLabel('Y:'), 8, 0)
        layout.addWidget(QLabel('every'), 8, 1)
        layout.addWidget(self.y_tick, 8, 2)
        layout.addWidget(self.ok_btn, 9, 1)
        self.d.setLayout(layout)
        self.ok_btn.clicked.connect(self.change_axes_plot)        
        self.d.exec()
        
    def change_axes_plot(self):
        x1 = float(self.x1_le.text())
        x2 = float(self.x2_le.text())
        y1 = float(self.y1_le.text())
        y2 = float(self.y2_le.text())  
        tick_span_x = float(self.x_tick.text())
        tick_span_y = float(self.y_tick.text())
        self.plot()
        self.ax.set_xlim(x1,x2)
        self.ax.set_ylim(y1,y2)
        x_ticks = self.frange(x1,x2,tick_span_x)
        y_ticks = self.frange(y1,y2,tick_span_y)
        self.ax.set_xticks(x_ticks)
        self.ax.set_yticks(y_ticks)
        self.ax.set_title(self.title.text())
        self.ax.set_xlabel(self.x_label.text())
        self.ax.set_ylabel(self.y_label.text())
        self.canvas.draw()
        
    def frange(self, start, stop, step):
        ticks = [start]
        i = start
        while i < stop:
            i += step
            ticks.append(i)
        return ticks