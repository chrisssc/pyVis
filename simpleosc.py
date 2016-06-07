################################################################################
###                                                                          ###
###                    Code to create Oscillator Superclass                  ###
###                                                                          ###
###        Generated waves are written into a buffer of size 2048.           ###
###      These smaller buffers are then concatenated into a larger buffer    ###
###                  which is written to a WAVE file.                        ###    
###                                                                          ###
################################################################################

import numpy as np
import scipy as sp

class Oscillator:
        
        def __init__(self, frequency, buffer_size, amplitude = 0.8,
                     sample_rate = 44100, bit_depth = 2**16):
                
                self.frequency = frequency
                self.amplitude = amplitude
                self.increment = buffer_size
                self.sample_rate = sample_rate
                self.bit_depth = bit_depth
                self.x = 0

        def __getitem__(self, idx):

                return self.LUT[idx]
        
        def update_buffer(self, long_buff, new_data):
			
                self.new_data = new_data
                self.long_buff = long_buff
                long_buff = np.append(long_buff, new_data)
                return long_buff
            
        def get_next(self):
			
                y = self.x
                self.x += self.increment
                return y
        
        def create_oscillator(self, arr, function):
                self.arr = arr
                ang_frequency = frequency * 2 * np.pi / float(self.sample_rate)
                z = self.get_next()
                for i in range(len(arr)):
                        arr[i] = ((i+z)*ang_frequency)
                arr = function(arr) * self.amplitude
                return arr
                        
