"""

RecursiveOscillator: a simple 2nd Order Recursive Oscillator

This is a subclass of the Oscillator class which can generate waves into
numpy array buffers when passed a function that defines the wave.


"""

__author__ = 'Chris Curry'
__version__ = '3.0'

from simpleosc import Oscillator
from simplebuffer import SoundBuffer
import numpy as np
import math as m


# The Recursive Oscillator takes an argument of resonant frequency in Hz and 
# calculates the angular frequency equivalent. Previous state values are 
# initially set to give the impression the Oscillator has been running forever,
# and are updated from the generate function once the programming is running

class RecursiveOscillator(Oscillator):

    # The setup method is used to set-up the initial state variables: y1 -
    # the sample at time 0 immediately preceding our first sine wave value; y2 - 
    # the sample before y1, given by calculating the amplitude of the sine wave
    # at the sample before time 0; omega_0 - the resonant frequency in radians
    # per second; and cos_omega_t, which is derived from our transfer function.

    def setup(self):
        
        """ Create the initial values needed to simulate infinite
            oscillation"""
        
        omega_0 = self.frequency*2.0*m.pi
        self.cos_omega_t = m.cos(omega_0/self.sample_rate)
        self.y2 = m.sin(-omega_0 / self.sample_rate)
        self.y1 = 0.0

    # A buffer is passed to the generate method and discrete output samples 
    # are calculated from the previous states using the transfer function, 
    # multiplied by the amplitude, and stored in the buffer which is then
    # returned as a numpy array.
    
    def generate(self, arr, length = None):
        
        """Generates a sine wave into a given buffer"""

        if length is None:
            length = len(arr)
            
        if length > len(arr):
            raise IndexError("Recursive Oscillator: buffer is too small!")

        if length < 1:
            raise IndexError("Recursive Oscillator: buffer can't be less than 1 sample")
        
        for i in range(length):
            
            y = (2*self.cos_omega_t)*self.y1-self.y2
            self.y2 = self.y1
            self.y1 = y
            arr[i] = y * self.amplitude
            
        return arr     
        
"""       
# Test Harness: Generate 8 seconds of 440Hz (A4) & write to .WAV file

buffer1 = SoundBuffer()
read_buffer = buffer1.create_buffer()

output_buffer = np.zeros(0)

osc1 = RecursiveOscillator(1000.0, buffer1.buffer_size)
osc1.setup()

time = int((8*(osc1.sample_rate))/ buffer1.buffer_size)
count = 0

while(count <= time):
        
        new_sine = osc1.generate(read_buffer)
        output_buffer = osc1.update_buffer(output_buffer, new_sine)
        count +=1

buffer1.write_file(output_buffer, "RecursiveOscillator2.wav")
print "Done!"
"""
