#!/usr/bin/env python
import Drone
import numpy as np

#==================
# MAIN ENTRY POINT
#==================

if __name__ == "__main__":
        try:
                p=Drone.photo("C:/Users/Ben/Desktop/4.tif")
                p.quadrat()
                count=p.count()
                print("count is : %d" %count)
        except ValueError, e:
                if e.message!= 'Failed to load OpenCL runtime':
                        raise ValueError, e



