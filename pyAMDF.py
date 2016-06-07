"""

pyAMDF: Average Magnitude Difference Function to detect fundamental frequency.


"""

__author__ = 'Chris Curry'
__version__ = '3.0'

import math as m
import numpy as np

class pyAMDF:

    def __init__(self, sample_rate = 48000, min_freq = 100.0,
                 max_freq = 4186.0, thresh = 40.0, ratio = 0.28):

        """ pyAMDF class calculates the fundamental frequency of a given chunk
        of audio data using the Average Magnitude Difference Function

        Parameters:

        sample_rate -- the sample rate of the input
        min_freq -- the minimum frequency which can be detected
        max_freq -- the maximum frequency which can be detected
        thresh -- the threshold for null detection
        ratio -- the change in threshold level for lower frequencies """

        self.min_freq = min_freq
        self.max_freq = max_freq
        self.sample_rate = sample_rate
        self.thresh = thresh
        self.ratio = ratio

    def detect(self, chunk):

        """ Detects the fundamental frequency of a given chunk of audio data by
        the AMDF method

        Parameters:

        chunk -- numpy array of audio data """

        data = chunk
        length = len(data)

        max_period = int(self.sample_rate / (self.min_freq + 0.5))
        min_period = int(self.sample_rate / (self.max_freq + 0.5))

        # amd is an integer array that holds average magnitude differences for
        # each offset value up to and including the max_period (lowest freq)

        amd = np.zeros(max_period + 1)

        # Try each offset from min to max and calculate AMD
        #
        # The data is 'time-shifted' forward by the offset using numpy's roll
        # method, allowing an element by element subtraction of the array and
        # its shifted equivalent. These difference values are stored in array
        # d, and the absolute magnitude of all of the differences is calculated.
        # The elements are then added together and stored in the amd array at
        # the sample equivalent to the offset value that has just been checked

        for o in range(min_period, max_period):

            data_shift = np.roll(data, -o)
            d = np.subtract(data[:(length/2)-o], data_shift[:(length/2)-o])
            d2 = np.absolute(d)
            amd[o] = np.sum(d2)


        # How can we ensure that we're getting the first minimum in any given
        # array of AMDF values? Need to set a threshold that can detect first
        # minimum when searching through the array. The amplitude of the first
        # null seems to increase as the source pitch increases. To counter-
        # act this we need to calculate the threshold as a function of the input
        # or reduce the range of frequencies which can be detected.
        #
        # The search length has to be small enough to detect even the highest
        # frequency that needs to be detected, therefore the search should be
        # the same length as the period of the highest frequency. If a null that
        # is below the threshold is detected in the search window we can assume
        # this is the fundamental (or at least an octave error).
        #
        # N.B. Uncomment print statement to check the fundamental detected


        search_length = min_period
        initial = self.thresh

        for i in range(min_period+1, max_period-search_length):

            if(min(amd[i:search_length+i]) < self.thresh):
                
                minimum = i + (np.argmin(amd[i:search_length+i]))
                fundamental = (self.sample_rate / minimum)
                #print("Fundamental is: " + str(fundamental))
                return fundamental

            self.thresh = (m.exp((-i * 0.01)) * initial)
        

        
    
