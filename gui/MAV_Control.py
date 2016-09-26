#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 13:43:10 2016

@author: fr0zty
"""
try:
    from PySide import QtCore, QtGui, QtUiTools
    from pyside_dynamic import loadUi
    import numpy as np
    import sys
    import os
    import warnings
    import subprocess
    import rospy
    
    
except ImportError:
    warnings.warn('Import Libraries missing')
    sys.exit()


class MAV_Control(QtGui.QMainWindow):
    '''
    GUI Controller Class for control over MAV
    '''
    def __init__(self):
        
        QtGui.QMainWindow.__init__(self)
        loadUi("GUI.ui", self)
        ros_topics = rospy.get_published_topics()
        
        self.config = ''
        self.tab_widget.setTabText(0, 'Simulation Control')
        self.tab_widget.setTabText(1, 'MAV Control')
        
        self.ls_topic_cb.addItems(ros_topics[0])
        self.st_r_cb.addItems(ros_topics[0])
        self.st_l_cb.addItems(ros_topics[0])
        self.set_label('','Black')
        self.quit_btn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        self.save_config_btn.clicked.connect(self.save_config_btn_clicked)
        self.reset_btn.clicked.connect(self.reset_btn_clicked)
        self.radio_controller.toggled.connect(self.radio_toggled)
        self.radio_controller_OA.toggled.connect(self.radio_toggled)
        
        self.radio_controller.setChecked(True)
        
    def radio_toggled(self):
        if self.radio_controller.isChecked():
            self.op_mode = 'rc'
            self.topics_widget.setEnabled(False)
        elif self.radio_controller_OA.isChecked():
            self.op_mode = 'rc_oa'
            self.topics_widget.setEnabled(True)
#__________________________________________________________________________________________________

#---------------------------------------Bottom Buttons---------------------------------------------
#__________________________________________________________________________________________________
    
    def reset_btn_clicked(self):
        self.ls_topic_cb.clear()
        self.st_r_cb.clear()
        self.st_l_cb.clear()
#__________________________________________________________________________________________________    
        
    def save_config_btn_clicked(self):
        pass

#__________________________________________________________________________________________________
    
    def load_config_btn_clicked(self):
        pass

    
#__________________________________________________________________________________________________

#---------------------------------------Extra Methods---------------------------------------------
#__________________________________________________________________________________________________

    def set_label(self, msg, color):
        assert type(color) == str, ' Color should be a String'
        assert type(msg) == str, 'message shoud be a String'
        self.status_label.setStyleSheet('color : %s;'%color)
        self.status_label.setText(msg)
    
    
    
#__________________________________________________________________________________________________    
    
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    MainWindow = MAV_Control()
    MainWindow.show()
    sys.exit(app.exec_())
