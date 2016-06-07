"""
pyVis: an interface to allow pitch and frequency information to be displayed
visually using pyprocessing.
"""

__author__ = 'Chris Curry'
__version__ = '3.0'

from pyprocessing import *
from simplePitchDetector import pitchDetector
from vuMeter import VUMeter
from simplebuffer import SoundBuffer
from RecursiveOscillator_v3 import RecursiveOscillator
import random as rand

noteColours = {'A': [153, 0, 51], 'A#': [0, 0, 255], 'B': [0, 127, 255],
               'C': [254, 254, 150],'C#':[153, 0, 255], 'D':[204, 102, 255],
               'D#':[0, 153, 0], 'E':[0, 255, 0], 'F': [255, 255, 64],
               'F#': [255, 255, 102], 'G':[255, 102, 51], 'G#':[255, 0, 0],
               }

### Test Harness: Sets up a sine wave at 440Hz (A4) for visualisation ###

sr = 48000      # Sample Rate
osc_amp = 0.99  # Amplitude of generated sine wave
bd = 2**15      # Bit depth

pd = pitchDetector(sr)
vu = VUMeter(bd)
bfr = SoundBuffer(1024)
osc = RecursiveOscillator(440.0, bfr.buffer_size, osc_amp, sr, bd)

osc.setup()
read_buffer = bfr.create_buffer()

def setup():

    """ Initialises the window size, colour, and transparency """
    
    background(0, 14)
    size(200,800)

def draw():

    """ This method is recursively called by pyprocessing, allowing the screen
    to be continuously updated with current information about the audio input's
    pitch and amplitude """
    
    # Initial rectangle fill is used to 'clear' the screen of old values
    
    fill(245,50)
    rect(0,0,width,height)
    fill(0)
    
    # Volume and pitch are calculated using methods in external classes
    #
    # In a real implementation, buf will be the result of calling a method that
    # continuously reads audio chunks into numpy arrays from a file or the
    # soundcard.

    # The Following chunk sets up a random frequency between 110Hz and 16kHz
    # which is then passed to an Oscillator instance & generated before having
    # its pitch value calculated & passed to the display output
    
    random_freq = float(rand.randint(110,16000))
    osc = RecursiveOscillator(random_freq, bfr.buffer_size, osc_amp, sr, bd)
    osc.setup()
    read_buffer = bfr.create_buffer()

    buf = osc.generate(read_buffer)
    volume = width * (abs(vu.get_SPL(buf))/80.0)
    note, octave = pd.get_pitch(buf)
    rgb = noteColours[note]
    pitch_pos = height - (height * (octave/12.0))

    # Define the RGB colour values as determine from the note value

    r = rgb[0]      # Red value
    g = rgb[1]      # Green value
    b = rgb[2]      # Blue value

    # As long as the input has an amplitude, visualise its pitch and amplitude 

    if(volume != 0):

        ypos = pitch_pos            # Vertical position defined by the pitch
        xpos = width/2              # Horizontal position is centered
        amp = volume                # Amplitude defined by volume

        stroke(r, g, b)             # RGB colour outline for the circle
        fill(0, 0, 0, 0)            # Transparent fill colour for the circle
        ellipse(xpos, ypos, amp, amp) # Draw the circle
        
        
run() # Let the visualisation begin




