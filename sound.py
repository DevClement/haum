import time
from pyo import *
# Initialize a Server object
s = Server().boot()
# Start playing audio
s.start()
# Plays the sine wave in Python console, returns immediately
a = Sine(mul=0.01).out()
time.sleep(3)
a.stop()