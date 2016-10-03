#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  2 15:02:51 2016

@author: fr0zty
"""
try:
    import rospy
    import rosgraph
    import rospkg
except ImportError as ie:
    print('Check ROS Installation', ie)

try:    
    import os
    import subprocess
    import json
    import sys
    import time
    import socket
    import warnings

except ImportError as ie:
    print('Import Libraries missing, install the specified library',ie)
    sys.exit()
#__________________________________________________________________________________________________

#------------------------------------------ROS Class-----------------------------------------------
#__________________________________________________________________________________________________

class ROS_Control(object):
    '''
    Python class for handling basic ROS Communications
    '''    
    def __init__(self):
        
        self.is_online = False
        self.ROS_MASTER_URI = ''
        self.ROS_PACKAGE_PATH = ''
    
    def check_rosmaster(self):
    
        try:
            rosgraph.Master('/rostopic').getPid()
            print('rosmaster running!')
            self.is_online = True
        except socket.error:
            warnings.warn('Unable to communicate with the master!')
            self.is_online = False
            
    def start_rosmaster(self):
        self.check_rosmaster()
        if self.is_online == True:
            warnings.warn('rosmaster already running')
        else:
            pass
            
    def get_package_path(self):
        self.ROS_MASTER_URI = rospkg.get_ros_package_path()
        
            
#            if config == None:
#                self.command = subprocess.Popen(['roscore'], stdout=subprocess.PIPE, shell=True)
#    #            out,err = command.communicate()
#    #            return out, err
#            elif config != None:
#                cmd1 = 'source %s'%config
#                cmd2 = 'roscore'
#                    
#                self.command = subprocess.Popen("{}; {}".format(cmd1, cmd2), shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
#    #            out, err = exec_cmd.communicate()
#    #            return out, err
#            
#        return rostopics        
        
    def kill_roscore(self):
        self.command.kill()
 
class ROSIOExecption(Exception):
    pass
        
        
if __name__ == '__main__':
    obj = ROS_Control()
    obj.check_rosmaster()