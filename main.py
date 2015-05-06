#!/usr/bin/env python
import Drone
import numpy as np

#==================
# MAIN ENTRY POINT
#==================

if __name__ == "__main__":
                p=Drone.photo("C:/Users/Ben/Dropbox/DJI01343.tif")
                p.quadrat()
                count=p.count()
                print("count is : %d" %count)