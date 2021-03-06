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
    import json
    import warnings
    import subprocess
    import rospy
#    from sim_test.classes import ROS_Control
except ImportError as ie:
    print('Import Libraries missing:', ie)
    sys.exit()

    
class MAV_Control(QtGui.QMainWindow):
    '''
    GUI Controller Class for control over MAV
    '''
    def __init__(self):
        
        QtGui.QMainWindow.__init__(self)
        loadUi("GUI.ui", self)
        
        self.output_directory = ''
        self.op_mode = ''
        self.config = ''
        self.ros_ok = False
        self.ros_config = ''
        self.ros_label.setStyleSheet('color : Red')
        self.ros_label.setText('OFFLINE')
#        self.twist_speed = self.twist_spinbox.value()
#        self.warning_threshold = self.warn_spinbox.value()
#        self.activation_threshold = self.auto_spinbox.value()
#        self.rate =
        self.keyslist = []

#        self.ls_topic_cb.addItems(self.ros_topics[0])
#        self.st_r_cb.addItems(self.ros_topics[0])
#        self.st_l_cb.addItems(self.ros_topics[0])
        self.set_label('','Black')
        self.quit_btn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        self.save_config_btn.clicked.connect(self.save_config_btn_clicked)
        self.output_btn.clicked.connect(self.output_directory_btn_clicked)
        self.reset_btn.clicked.connect(self.reset_btn_clicked)
        self.radio_controller.toggled.connect(self.radio_toggled)
        self.radio_controller_OA.toggled.connect(self.radio_toggled)
#        self.twist_spinbox.valueChanged.connect(self.spinbox_value_changed)
#        self.warn_spinbox.valueChanged.connect(self.spinbox_value_changed)
#        self.auto_spinbox.valueChanged.connect(self.spinbox_value_changed)
#        self.rate_spinbox.valueChanged.connect(self.spinbox_value_changed)        
        
        self.controller_widget.setEnabled(True)
        self.radio_controller.setChecked(True)


        
#__________________________________________________________________________________________________
        
    def operation_mode(self):
        if self.mav_radio.isChecked():
            self.gazebo_config_widget.setEnabled(False)
            self.mav_widget.setEnabled(True)
            self.sim_widget.setEnabled(False)
        if self.sim_radio.isChecked():
            self.mav_widget.setEnabled(True)
            self.gazebo_widget.setEnabled(True)
            self.sim_widget.setEnabled(False)

    def radio_toggled(self):
        if self.radio_controller.isChecked():
            self.op_mode = 'rc'
            self.topics_widget.setEnabled(False)
            self.auto_widget.setEnabled(False)
            self.warn_widget.setEnabled(False)
        elif self.radio_controller_OA.isChecked():
            self.op_mode = 'rc_oa'
            self.topics_widget.setEnabled(True)
            self.auto_widget.setEnabled(True)
            self.warn_widget.setEnabled(True)

#__________________________________________________________________________________________________                        
    def ros_config_btn_clicked(self):
        self.ros_text_field.setText((QtGui.QFileDialog.getOpenFileName(self, 'ROS Configutaion', self.output_dir, '*.bash')[0]))
        self.ros_config = self.ros_text_field.text()
        
    def output_directory_btn_clicked(self):
        self.output_dir_txt_field.setText(self.dir_dialog(self.output_directory))
        self.output_directory = self.output_dir_txt_field.text()        
        
#__________________________________________________________________________________________________

#    def spinbox_value_changed(self):
#        self.twist_speed = self.twist_spinbox.value()
#        self.warning_threshold = self.warn_spinbox.value()
#        self.activation_threshold = self.auto_spinbox.value()
#        self.rate = self.rate_spinbox.value()

        
#__________________________________________________________________________________________________

#-----------------------------------Central controls and Labels------------------------------------
#__________________________________________________________________________________________________                
    def set_status_values(self):
        if self.ros_ok:
            self.ros_label.setStyleSheet('color: Green')
            self.ros_label.setText('ONLINE')

        
    def keyPressEvent(self, event):
        if type(event) == QtGui.QKeyEvent:
            self.firstrelease = True
            print(event.key())
            self.set_label('%s'%event.key(),'Red')
            event.accept()
        else:
            event.ignore()

    def keyReleaseEvent(self, event):
        if self.firstrelease == True:
            self.processmultikeys(self.keyslist)
        self.firstrelease = False
        del self.keyslist[-1]
            
    def processmultikeys(self,keyspressed):
        print(keyspressed)
#__________________________________________________________________________________________________

#---------------------------------------Bottom Buttons---------------------------------------------
#__________________________________________________________________________________________________
    
    def reset_btn_clicked(self):
    
        self.output_dir_txt_field.setText('')
        self.twist_spinbox.setValue(1)
        self.warn_spinbox.setValue(4)
        self.activation_threshold.setValue(2)
        self.ls_topic_cb.clear()
        self.st_r_cb.clear()
        self.st_l_cb.clear()
        self.ros_text_field.setText('')
        
        self.output_directory = ''
        self.config = ''
        self.ros_config = ''
        self.warning_threshold = self.warn_spinbox.value()
        self.activation_threshold = self.auto_spinbox.value()
        
        
        self.radio_controller.setChecked(True)
#__________________________________________________________________________________________________    
        
    def save_config_btn_clicked(self):
    
        if ~self.check_fields():
            self.set_label('Please select an output directory', 'Red')
        else:
            config = {}
            config['operation_mode'] = self.op_mode
            config['output_directory'] = self.output_directory
            config['laser_scan_topic'] = str(self.ls_topic_cb.currentText())
            config['stereo_cam_right_topic'] = str(self.st_l_cb.currentText())
            config['stereo_cam_left_topic'] = str(self.st_r_cb.currentText())
            
            file_name = os.path.join(self.output_directory, 'mav_configuration.json')
            self.config = 'mav_configuration.json'
            
            with open(file_name, mode='w') as f:
                json.dump(config, f)
#__________________________________________________________________________________________________
    
    def load_config_btn_clicked(self):

        if self.output_dir_txt_field.text() != '':
            self.output_directory = self.output_dir_txt_field.text()
        
        if self.config == '':
            self.config = os.path.join(self.output_directory, 'mav_configuration.json')
            
        try:
            with open(self.config) as f:
                json_obj = json.load(f)
            self.op_mode = json_obj.get('operation_mode')
            
            if self.op_mode == 'rc':
                self.radio_controller.setChecked(True)
            elif self.op_mode == 'rc_oa':
                self.radio_controller_OA.setChecked(True)
            else:
                print('Invalid Operation Mode')
                self.set_label('Invalid Operation Mode','Red')
            
            self.output_dir_txt_field.setText(json_obj.get('output_directory'))
            self.output_directory = json_obj.get('output_directory')
            
   ## check ros_topics var         
            
#            if json_obj.get('laser_scan_topic') in self.ros_topics[0]:
#                index = self.ls_topic_cb.findText(json_obj.get('laser_scan_topic'), QtCore.Qt.MatchFixedString)
#                if index >= 0:
#                    self.ls_topic_cb.setCurrentIndex(index)
#            
#            if json_obj.get('stereo_cam_right_topic') in self.ros_topics[0]:
#                index = self.st_r_cb.findText(json_obj.get('stereo_cam_right_topic'), QtCore.Qt.MatchFixedString)
#                if index >= 0:
#                    self.st_r_cb.setCurrentIndex(index)
#                    
#            if json_obj.get('stereo_cam_left_topic') in self.ros_topics[0]:
#                index = self.st_l_cb.findText(json_obj.get('stereo_cam_left_topic'), QtCore.Qt.MatchFixedString)
#                if index >= 0:
#                    self.st_l_cb.setCurrentIndex(index)
            
        except IOError as ioe:
            print('File not found', ioe)
            self.set_label('Configuration file not found', 'Red')
        except IndexError as iee:
            print('Invalid Key in configuration file', iee)
            self.set_label('Invalid key in configuration file', 'Red')
#__________________________________________________________________________________________________

    

#---------------------------------------Extra Methods----------------------------------------------
#__________________________________________________________________________________________________

    def systems_check(self):
        '''
        Check all system initializations on start
        '''
        pass

#__________________________________________________________________________________________________

    def set_label(self, msg, color):
        self.status_label.setStyleSheet('color : %s;'%color)
        self.status_label.setText(msg)

#__________________________________________________________________________________________________
        
    def check_fields(self):
        if self.output_dir_txt_field.text() == '':
            return False
        else:
            return True
#__________________________________________________________________________________________________

#---------------------------------------Static Methods---------------------------------------------
#__________________________________________________________________________________________________        
 
    @staticmethod
    def dir_dialog(dir_loc):
        '''
        Directory dialog method for selection of directory
        '''
        dialog = QtGui.QFileDialog()
        if dir_loc == '':
            dir_name = dialog.getExistingDirectory(None, 'Select a Directory', os.getcwd(), QtGui.QFileDialog.ShowDirsOnly)
        else:
            dir_name = dialog.getExistingDirectory(None, 'Select a Directory', dir_loc, QtGui.QFileDialog.ShowDirsOnly)
        return dir_name 

#__________________________________________________________________________________________________    

    @staticmethod
    def check_status(status_flag, quadrant):
        pass
#        if status_flag == 1:
#            self.set_label('Warning: Object detected closer than Warning Threshold %d'%self.warning_threshold)

 
#__________________________________________________________________________________________________    
    
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    
    MainWindow = MAV_Control()
    MainWindow.show()
    sys.exit(app.exec_())
