"""

vuMeter: detects the Sound Pressure Level of a given input in a fashion similar
to VU meters on mixing desks
"""
__author__ = 'Chris Curry'
__version__ = '3.0'

import math as m
import numpy as np

class VUMeter:

    def __init__(self, bit_depth = 2**15):

        self.bit_depth = bit_depth

    def get_SPL(self, arr):

        """

        Audio data is scaled by its bit depth into a numpy array of float
        values, and the RMS value is calculated. This RMS value is then used to
        calculate the sound pressure level in decibels.

        Parameters:

        arr -- input array of 16-bit audio data
        
        """
        
        data = np.array(arr, dtype=float) / self.bit_depth
        rms = m.sqrt(np.sum(data ** 2.0) / len(data))
        
        if rms < 10e-8:

            # This prevents the log calculation from returning values quieter
            # than -80dB, as this is practically inaudible

            rms = 10e-8

        return 10.0 * m.log(rms, 10.0)




    
