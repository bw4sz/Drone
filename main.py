#!/usr/bin/env python
import Drone
import numpy as np

#==================
# MAIN ENTRY POINT
#==================

if __name__ == "__main__":
        while True:
                try:
                        p=Drone.photo("C:/Users/Ben/Desktop/4.tif")
                        img=Drone.photo.quadrat(p)
                        count=Drone.photo.count(img)
                        print("count is : %d" %count)
                except ValueError, e:
                        if e.message!= 'Failed to load OpenCL runtime':
                                raise ValueError, e



