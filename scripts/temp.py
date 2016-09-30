#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 19 11:08:48 2016

@author: fr0zty
"""
import numpy as np
import warnings


class Obstacle_Avoidance(object):

    def __init__(self):

        self.warning_threshold = 4
        self.auto_threshold = 2
        self.laser_unsafe_quads = np.zeros(6, dtype=np.bool)
        self.laser_warning_quads = np.zeros(6, dtype=np.bool)
        self.stereo_unsafe_quads = np.zeros(2, dtype=np.bool)
        self.stereo_warning_quads = np.zeros(2, dtype=np.bool)
        self.twist_speed = 1
        self.status_flag = 0 # status_flag: 0 -> safe, 1 -> warning, 2 -> automatic controller

    def get_safe_quadrant(self, laser_data, depth_map):

        self.laser_quadrants = np.array(np.split(laser_data, 6))
        self.depth_map_quadrants = np.array(np.split(depth_map, 2))
        laser_warn_cond = (self.laser_quadrants <= self.warning_threshold and self.laser_quadrants >= self.auto_threshold)
        laser_auto_cond = (self.laser_quadrants <= self.auto_threshold)

        depth_warn_cond = (self.depth_map_quadrants <= self.warning_threshold and self.depth_map_quadrants >= self.auto_threshold)
        depth_auto_cond = (self.depth_map_quadrants <= self.warning_threshold and self.depth_map_quadrants >= self.auto_threshold)

        for i in xrange(6):

            if any(laser_warn_cond[i,:]):

                self.laser_warning_quads[i] = True
                self.status_flag = 1

            if any(laser_auto_cond[i,:]):

                self.laser_unsafe_quads[i] = True
                self.status_flag = 2

        for j in xrange(2):

            if any(depth_warn_cond[j,:]):
                self.stereo_warning_quads[j] = True
                self.status_flag = 1

            if any(depth_auto_cond[j,:]):
                self.stereo_unsafe_quads[j] = True
                self.status_flag = 2

        warning_quadrants = np.hstack((self.stereo_warning_quads[1], self.laser_warning_quads, self.stereo_warning_quads[0]))
        unsafe_quadrants = np.hstack((self.stereo_unsafe_quads[1], self.laser_unsafe_quads, self.stereo_unsafe_quads[0]))
        safe_quadrants = np.argwhere(~unsafe_quadrants)

        if len(warning_quadrants >= 1):
            print('Warning')

        if len(safe_quadrants) > 1:
            mean_ary = np.zeros(len(safe_quadrants))
            for i in xrange(len(safe_quadrants)):
                mean_ary[i] = np.mean(self.laser_quadrants[safe_quadrants[i]])

            self.quadrant = np.argmax(mean_ary)

        elif len(safe_quadrants) == 1:
            if safe_quadrants <= 3:
                self.quadrant += 4
            elif safe_quadrants >= 4:
                self.quadrant -= 4
        else:
            print('No safe quadrants')


    def get_twist_msg(self, twist_velocity):
        if self.quadrant == 0:
            return np.array([0.25*twist_velocity, 0.75*twist_velocity, 0])
        elif self.quadrant == 1:
            return np.array([0.75*twist_velocity, 0.25*twist_velocity, 0])
        elif self.quadrant == 2:
            return np.array([0.75*twist_velocity, -0.25*twist_velocity, 0])
        elif self.quadrant == 3:
            return np.array([0.25*twist_velocity, -0.75*twist_velocity, 0])
        elif self.quadrant == 4:
            return np.array([-0.25*twist_velocity, -0.75*twist_velocity, 0])
        elif self.quadrant == 5:
            return np.array([-0.75*twist_velocity, -0.25*twist_velocity, 0])
        elif self.quadrant == 6:
            return np.array([-0.75*twist_velocity, 0.25*twist_velocity, 0])
        elif self.quadrant == 7:
            return np.array([-0.26*twist_velocity, 0.75*twist_velocity, 0])
        else:
            return np.array[0.0, 0.0, 0.0]




if __name__ == '__main__':

    unsafe_quadrants = np.zeros(8, dtype=np.bool)

    unsafe_quadrants[0] = False
    unsafe_quadrants[1] = True
    unsafe_quadrants[2] = False
    unsafe_quadrants[3] = True
    unsafe_quadrants[4] = False
    unsafe_quadrants[5] = True
    unsafe_quadrants[6] = False
    unsafe_quadrants[7] = True





