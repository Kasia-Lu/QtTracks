# -*- coding: utf-8 -*-
"""
AFTcalc is a PyQt5 App to calculate apatite fission track ages
and to create plots for data analysis, including a radial plot.

Created on Wed Feb 20 11:23:28 2019

@author: Katarzyna Luszczak
"""

import sys

from PyQt5.Qt import QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QVBoxLayout,
                             QWidget,
                             QMenu,
                             QTabWidget,
                             QMainWindow,
                             QFileDialog, 
                             QMessageBox,
                             QAction)

from Histogram import Histogram
from Sample_Info import Sample_Info
from Age_DPar_plot import Age_DPar_plot
from Ns_UCa_plot import Ns_UCa_plot
from Ns_Ni_plot import Ns_Ni_plot
from Multi_plot import Multi_plot
from Radial_plot import Radial_plot
from KDE_plot import KDE_plot
from Age_Data_Window import Age_Data_Window
from Length_Data_Window import Length_Data_Window

#------------------------------------------------------------------------------
class Main_Window(QMainWindow):

    def __init__(self):
        super(Main_Window, self).__init__()
        self.setGeometry(500, 150, 600, 700)
        self.setWindowTitle('Qt Tracks')
        self.setWindowIcon(QIcon('icons/cat-icon.png'))
        
        self.tabs_widget = Tabs_Widget(self)
        self.sample_info = self.tabs_widget.sample_info

        self.setCentralWidget(self.tabs_widget)
        
        self.menubar()
        
    def menubar(self):
        mainMenu = self.menuBar()
                
        Action_laser_data = QAction('LA-ICP-MS zeta method', self)
        Action_laser_data.setStatusTip('Open file with LA-ICP-MS data for zeta method')
        Action_laser_data.triggered.connect(self.open_la_data_file)
        
        Action_edm_data = QAction('External detector method', self)    
        Action_edm_data.setStatusTip('Open file with track count data for external detector method')
        Action_edm_data.triggered.connect(self.open_edm_data_file)
        
        Submenu_open_age_data = QMenu('Open age data file', self)
        Submenu_open_age_data.addAction(Action_laser_data)
        Submenu_open_age_data.addAction(Action_edm_data)
        
        Action_open_length_data = QAction('Open length data file', self)
        #Action_open_data.setShortcut('Ctrl+O')
        Action_open_length_data.setStatusTip('Open file with length data')
        Action_open_length_data.triggered.connect(self.open_length_data_file)
        
        Action_save_data = QAction('Save data', self)
        Action_save_data.setShortcut('Ctrl + S')
        Action_save_data.setStatusTip('Save calculated AFT data into a csv file')
        Action_save_data.triggered.connect(self.save_data)
        
        Action_save_plot = QAction('Save plot', self)
        Action_save_plot.setStatusTip('Save generated plot into a PNG or PDF file')
        Action_save_plot.triggered.connect(self.save_plot)
        
        Action_quit = QAction('Exit', self)
        Action_quit.setShortcut('Ctrl + Q')
        Action_quit.setStatusTip('Leave The App')
        Action_quit.triggered.connect(self.close_application)
                      
        Action_copy = QAction('Copy', self)
        Action_copy.setShortcut('Ctrl + C')
        Action_copy.setStatusTip('Copy to clipboard')
        Action_copy.triggered.connect(self.copy_data)
        
        Action_paste = QAction('Paste', self)
        Action_paste.setShortcut('Ctrl + Q')
        Action_paste.setStatusTip('Paste from clipboard')
        Action_paste.triggered.connect(self.paste_data)
        
        Action_delete = QAction('Cut', self)
        Action_delete.setShortcut('Ctrl + X')
        Action_delete.setStatusTip('Delete...')
        Action_delete.triggered.connect(self.delete_data)
        
        Action_Ns_Ni = QAction('Ns vs. Ni Scatter', self)
        Action_Ns_Ni.setStatusTip('Plot Ns vs. Ni scatter')
        Action_Ns_Ni.triggered.connect(self.Ns_Ni_plot_init)
        Action_Ns_Ni.setEnabled(False)
        
        Action_Ns_UCa = QAction('Ns vs. U/Ca Scatter', self)
        Action_Ns_UCa.setStatusTip('Plot Ns vs. U/Ca ratio scatter')
        Action_Ns_UCa.triggered.connect(self.Ns_UCa_plot_init)
        Action_Ns_UCa.setEnabled(False)
        
        Action_age_DPar = QAction('Age vs. DPar Scatter', self)
        Action_age_DPar.setStatusTip('Plot Age vs. DPar scatter')
        Action_age_DPar.triggered.connect(self.age_dpar_plot_init)
        Action_age_DPar.setEnabled(False)
        
        Action_KDE_ages = QAction('KDE', self)
        Action_KDE_ages.setStatusTip('Plot KDE plot of AFT ages')
        Action_KDE_ages.triggered.connect(self.KDE_plot_init)
        Action_KDE_ages.setEnabled(False)
        
        Action_radial_plot = QAction('Radial Plot', self)
        Action_radial_plot.setStatusTip('Create a radial plot for loaded data')
        Action_radial_plot.triggered.connect(self.radial_plot_init)
        Action_radial_plot.setEnabled(False)
        
        Action_multi_plot = QAction('Multi plot', self)
        Action_multi_plot.setStatusTip('Create a multi plot with chosen plots')
        Action_multi_plot.triggered.connect(self.multi_plot_init)
        Action_multi_plot.setEnabled(False)

        Action_lengths_m_hist = QAction('Measured track lengths', self)
        Action_lengths_m_hist.setStatusTip('Create a track length histogram for measured track lengths')
        Action_lengths_m_hist.triggered.connect(self.lengths_m_hist_init)
        Action_lengths_m_hist.setEnabled(False)
        
        Action_lengths_p_hist = QAction('Projected track lengths', self)
        Action_lengths_p_hist.setStatusTip('Create a track length histogram for projected track lengths')
        Action_lengths_p_hist.triggered.connect(self.lengths_p_hist_init)
        Action_lengths_p_hist.setEnabled(False)
        
        Submenu_histograms = QMenu('Track lengths histogram', self)
        Submenu_histograms.addAction(Action_lengths_m_hist)
        Submenu_histograms.addAction(Action_lengths_p_hist)
        
        fileMenu = mainMenu.addMenu('File')
        fileMenu.addMenu(Submenu_open_age_data)
        fileMenu.addAction(Action_open_length_data)
        fileMenu.addAction(Action_save_data)
        fileMenu.addAction(Action_save_plot)
        fileMenu.addAction(Action_quit)
        
        editorMenu = mainMenu.addMenu('Edit')
        editorMenu.addAction(Action_copy)
        editorMenu.addAction(Action_paste)
        editorMenu.addAction(Action_delete)
        
        plotsMenu = mainMenu.addMenu('Plots')
        plotsMenu.addAction(Action_Ns_Ni)
        plotsMenu.addAction(Action_Ns_UCa)
        plotsMenu.addAction(Action_age_DPar)
        plotsMenu.addAction(Action_KDE_ages)
        plotsMenu.addAction(Action_radial_plot)
        plotsMenu.addMenu(Submenu_histograms)
        plotsMenu.addAction(Action_multi_plot)
        
        self.plots_menu_items = [Action_Ns_Ni,
                                 Action_Ns_UCa,
                                 Action_age_DPar,
                                 Action_KDE_ages,
                                 Action_radial_plot,
                                 Action_multi_plot,
                                 Action_lengths_m_hist,
                                 Action_lengths_p_hist]
        
        self.statusBar()
        self.show()
        
    def open_la_data_file(self):
        self.tabs_widget.tabs.addTab(self.tabs_widget.tab2, 'Age data')
        self.tabs_widget.tab2.layout = QVBoxLayout(self)
        self.Age_Data_Window = Age_Data_Window(data_type='LA', plots_menu_items=self.plots_menu_items)
        self.tabs_widget.tab2.layout.addWidget(self.Age_Data_Window)
        self.tabs_widget.tab2.setLayout(self.tabs_widget.tab2.layout)
        
    def open_edm_data_file(self):
        self.tabs_widget.tabs.addTab(self.tabs_widget.tab7, 'Age data')
        self.tabs_widget.tab7.layout = QVBoxLayout(self)
        self.Age_Data_Window = Age_Data_Window(data_type='EDM', plots_menu_items=self.plots_menu_items)
        self.tabs_widget.tab7.layout.addWidget(self.Age_Data_Window)
        self.tabs_widget.tab7.setLayout(self.tabs_widget.tab7.layout)
        
    def open_length_data_file(self):
        self.tabs_widget.tabs.addTab(self.tabs_widget.tab3, 'Length data')
        self.tabs_widget.tab3.layout = QVBoxLayout(self)
        self.Length_Data_Window = Length_Data_Window(plots_menu_items=self.plots_menu_items)
        self.tabs_widget.tab3.layout.addWidget(self.Length_Data_Window)
        self.tabs_widget.tab3.setLayout(self.tabs_widget.tab3.layout)
        
    def save_data(self):
        name, _ = QFileDialog.getSaveFileName(self, 'Save File')
        file = open(name,'w')
        text = self.textEdit.toPlainText()
        file.write(text)
        file.close()
        
    def save_plot(self):
        name, _ = QFileDialog.getSaveFileName(self, 'Save File')
        file = open(name, 'w')
        text = self.textEdit.toPlainText()
        file.write(text)
        file.close()
        
    def close_application(self):
        choice = QMessageBox.question(self, 'Quitting...',
                                            'Are you sure you want to quit?',
                                            QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            sys.exit()
        else:
            pass
    
    def Ns_Ni_plot_init(self):
        self.tabs_widget.tabs.addTab(self.tabs_widget.tab10, 'Ns vs Ni')
        self.tabs_widget.tab10.layout = QVBoxLayout(self)
        self.tabs_widget.tab10.layout.addWidget(Ns_Ni_plot(data_in=self.Age_Data_Window.a_data))
        self.tabs_widget.tab10.setLayout(self.tabs_widget.tab10.layout)

    def Ns_UCa_plot_init(self):
        self.tabs_widget.tabs.addTab(self.tabs_widget.tab9, 'Ns vs U/Ca')
        self.tabs_widget.tab9.layout = QVBoxLayout(self)
        self.tabs_widget.tab9.layout.addWidget(Ns_UCa_plot(data_in=self.Age_Data_Window.a_data))
        self.tabs_widget.tab9.setLayout(self.tabs_widget.tab9.layout)
    
    def age_dpar_plot_init(self):
        self.tabs_widget.tabs.addTab(self.tabs_widget.tab8, 'Age vs DPar')
        self.tabs_widget.tab8.layout = QVBoxLayout(self)
        self.tabs_widget.tab8.layout.addWidget(Age_DPar_plot(data_in=self.Age_Data_Window.a_data))
        self.tabs_widget.tab8.setLayout(self.tabs_widget.tab8.layout)
        
    def KDE_plot_init(self):
        self.tabs_widget.tabs.addTab(self.tabs_widget.tab11, 'KDE plot')
        self.tabs_widget.tab11.layout = QVBoxLayout(self)
        self.tabs_widget.tab11.layout.addWidget(KDE_plot(data_in=self.Age_Data_Window.a_data))
        self.tabs_widget.tab11.setLayout(self.tabs_widget.tab11.layout)
        
    def radial_plot_init(self):
        self.tabs_widget.tabs.addTab(self.tabs_widget.tab4, 'Radial Plot')
        self.tabs_widget.tab4.layout = QVBoxLayout(self)
        self.tabs_widget.tab4.layout.addWidget(Radial_plot(data_in=self.Age_Data_Window.a_data, 
                                                           sample_name=self.sample_info.sample_name))
        self.tabs_widget.tab4.setLayout(self.tabs_widget.tab4.layout)
        
    def lengths_m_hist_init(self):       
        self.tabs_widget.tabs.addTab(self.tabs_widget.tab5, 'Histogram')
        self.tabs_widget.tab5.layout = QVBoxLayout(self) 
        self.tabs_widget.tab5.layout.addWidget(Histogram(data_in=self.Length_Data_Window.l_data))
        self.tabs_widget.tab5.setLayout(self.tabs_widget.tab5.layout)
        
    def lengths_p_hist_init(self):       
        self.tabs_widget.tabs.addTab(self.tabs_widget.tab6, 'Histogram')
        self.tabs_widget.tab6.layout = QVBoxLayout(self)
        self.tabs_widget.tab5.layout.addWidget(Histogram(data_in=self.Length_Data_Window.l_data))
        self.tabs_widget.tab6.setLayout(self.tabs_widget.tab6.layout)
        
    def multi_plot_init(self):
        self.tabs_widget.tabs.addTab(self.tabs_widget.tab12, 'Multi-plot')
        self.tabs_widget.tab12.layout = QVBoxLayout(self)
        self.tabs_widget.tab12.layout.addWidget(Multi_plot(data_in=self.Age_Data_Window.a_data))
        self.tabs_widget.tab12.setLayout(self.tabs_widget.tab12.layout)
        
    def copy_data(self):
        pass        #temporary code
    
    def paste_data(self):
        pass        #temporary code
    
    def delete_data(self):
        pass        #temporary code
        
#------------------------------------------------------------------------------      
class Tabs_Widget(QWidget):
     
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
         
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.tab5 = QWidget()
        self.tab6 = QWidget()
        self.tab7 = QWidget()
        self.tab8 = QWidget()
        self.tab9 = QWidget()
        self.tab10 = QWidget()
        self.tab11 = QWidget()
        self.tab12 = QWidget()
       
        self.tabs.addTab(self.tab1, 'Sample info')
        self.tab1.layout = QVBoxLayout(self)
        self.sample_info = Sample_Info()
        self.tab1.layout.addWidget(self.sample_info)
        self.tab1.setLayout(self.tab1.layout)
        
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        
    def close_tab(self, index):
        tab = self.tabs.widget(index)
        tab.deleteLater()
        self.tabs.removeTab(index)

#------------------------------------------------------------------------------
def run():
    app = QApplication(sys.argv)
    GUI = Main_Window()
    sys.exit(app.exec_())

run()