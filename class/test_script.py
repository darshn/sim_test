#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  4 16:36:51 2016

@author: fr0zty
"""

import numpy as np

def get_twist(twist_velocity,key_events, controls=['w', 's', 'a', 'd', 'up', 'dn', 'lf' , 'rt']):
    
    dx, dy, dz = twist_velocity
    dax, day, daz = twist_velocity
    
    twist_events = {  #x, y, z, pitch, roll, yaw
                    controls[0]: [dx, 0, 0, 0, 0, 0],
                    controls[1]: [-dx, 0, 0, 0, 0, 0],
                    controls[2]: [0, dy, 0, 0, 0, 0],
                    controls[3]: [0, -dy, 0, 0, 0, 0], 
                    controls[4]: [0, 0, dz, 0, 0, 0],
                    controls[5]: [0, 0, -dz, 0, 0, 0],
                    controls[6]: [0, 0, 0, 0, 0, daz],
                    controls[7]: [0, 0, 0, 0, 0, -daz],
                    }
    return twist_events[key_events]

x = get_twist(2, 'w', controls=['w', 's', 'a', 'd', 'up', 'dn', 'lf' , 'rt'])
