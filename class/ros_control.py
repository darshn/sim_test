#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  2 15:02:51 2016

@author: fr0zty
"""
try:
    import rospy
except ImportError as ie:
    print('Check ROS Installation', ie)
try:
    import os
    import subprocess
    import json
    import sys
    import time
except ImportError as ie:
    print('Import Libraries missing, install the specified library',ie)
    sys.exit()
class ROS_Control(object):
    def __init__(self):
        
        self.ros_online = False
        self.ros_topics = []
        
    def start_ros(self, config=None):
        if config == None:
            self.command = subprocess.Popen(['roscore'], stdout=subprocess.PIPE, shell=True)
#            out,err = command.communicate()
#            return out, err
        elif config != None:
            cmd1 = 'source %s'%config
            cmd2 = 'roscore'
                
            self.command = subprocess.Popen("{}; {}".format(cmd1, cmd2), shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
#            out, err = exec_cmd.communicate()
#            return out, err
        rostopics = rospy.get_published_topics()
            
        return rostopics
        
    def kill_roscore(self):
        self.command.kill()
        
        
        
if __name__ == '__main__':
    obj = ROS_Control()
    a = obj.start_ros()
    obj.kill_roscore()
