################################################################################
###                                                                          ###
###                       Code to create a Resuable Buffer                   ###
###                                                                          ###
###        Generated waves are written into a buffer of size 2048.           ###
###      These smaller buffers are then concatenated into a larger buffer    ###
###                  which is written to a WAVE file.                        ###    
###                                                                          ###
################################################################################

import numpy as np
import scipy as sp
import scipy.io.wavfile

class SoundBuffer:
        
        def __init__(self, buffer_size = 2048):
                self.buffer_size = buffer_size
                self.x = 0
                
        def create_buffer(self):
                the_buffer = np.zeros(self.buffer_size)
                return the_buffer

        def get_next(self):
                y = self.x
                self.x += self.buffer_size
                return y
        
        def write_file(self, long_buff, filename, sample_rate = 44100):
                self.long_buff = long_buff
                self.sample_rate = sample_rate
                convert_16_bit = float(2**15)
                long_buff = np.int16( long_buff * convert_16_bit )
                scipy.io.wavfile.write(filename,
                                       sample_rate, long_buff)

        def read_file(self, filename, chunk):

                convert_16_bit = float(2**15)
                wavFile = scipy.io.wavfile.read(filename)
                read_buffer = np.int16(wavFile.data * convert_16_bit)
                output_buffer = np.zeros(self.buffer_size)

                """

                offset = self.get_next()
                
                if ((offset+len(chunk)) < len(read_buffer)):
                        
                        output_buffer = read_buffer[offset:(offset+len(chunk)-1)]
                        
                        return output_buffer
                """

                return read_buffer
