"""

vuMeter: detects the Sound Pressure Level of a given input in a fashion similar
to VU meters on mixing desks
"""

import math as m
import numpy as np

class VUMeter:

    def __init__(self, bit_depth = 2**15):

        self.bit_depth = bit_depth

    def get_SPL(self, arr):

        """

        16-bit data is scaled into a numpy array of float values,
        all elements are squared, then added together, and the square
        root of this sum is taken. The value is then divided by the length
        of the numpy array and the dB SPL value is returned

        Parameters:

        arr -- input array of 16-bit audio data
        
        """
        
        data = np.array(arr, dtype=float) / self.bit_depth
        ms = m.sqrt(np.sum(data ** 2.0) / len(data))
        
        if ms < 10e-8:

            ms = 10e-8

        return 10.0 * m.log(ms, 10.0)




    
