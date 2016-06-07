"""

simplePitchDetector: a class to detect the pitch of audio using the AMDF
method.

"""

__author__ = 'Chris Curry'
__version__ = '3.14'

import math as m
import numpy as np
from pyAMDF import *

class pitchDetector:

    def __init__(self, sample_rate = 48000):

        self.sample_rate = sample_rate

    def detect_pitch(self, buf):

        """
        Detects the fundamental frequency of a chunk of audio data using the
        AMDF method.

        Paramaters:

        buf -- a numpy array filled with audio data """
        
        amdf = pyAMDF(self.sample_rate)
        the_min = amdf.detect(buf)
        return the_min

    def get_MIDI(self, freq):

        """
        Calculates the MIDI number for a particular pitch in the range 0-127

        Parameters:

        freq -- the fundamental frequency of the note """
        
        if freq is None:
            
            return None
        else:
            return (69 + 12 * (m.log((freq / 440.0), 2.0)))




