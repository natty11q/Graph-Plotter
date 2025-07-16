from Maths.Maths import *
import numpy


class P_Function:
    def __init__(self):
        self.axies      : list[str] = ["X","Y"]
        self.ranges     : list[list[float]]  # ranges for each axis (calculated)
        self.divisions  : list[list[float]]  # divisions for each axis (calculated)
    
        self.samplePoints   : list[numpy.ndarray] # points from each axis stored in the array

    def Update(self):
        ...