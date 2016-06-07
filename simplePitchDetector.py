"""

simplePitchDetector: a class to detect the pitch of audio using the AMDF
method.

"""

__author__ = 'Chris Curry'
__version__ = '3.14'

import math as m
import numpy as np
from pyAMDF import *

midiLookup = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']

class pitchDetector():

    def __init__(self, sample_rate = 48000):

        self.sample_rate = sample_rate

    def detect_fundamental(self, buf):

        """
        Detects the fundamental frequency of a chunk of audio data using the
        AMDF method.

        Paramaters:

        buf -- a numpy array filled with audio data """
        
        amdf = pyAMDF(self.sample_rate)
        freq = amdf.detect(buf)
        return freq

    def get_MIDI_num(self, freq):

        """
        Calculates the MIDI number for a particular pitch in the range 0-127

        Parameters:

        freq -- the fundamental frequency of the note """
        
        if freq is None:
            
            return None
        else:
            self.midi = int((69 + 12 * (m.log((freq / 440.0), 2.0))))
            return self.midi


    def get_pitch(self, buf):

        """
        Calculates the Note value by establishing the integer remainder of the
        MIDI number divided by 12, and calculates the Octave by establishing how
        many times 12 can be evenly divided into the MIDI number

        Parameters:

        buf -- a numpy array filled with audio data """

        freq = self.detect_fundamental(buf)
        self.midi = self.get_MIDI_num(freq)
        note = midiLookup[self.midi%12]
        octave = int(self.midi/12)
        return note, octave
        




