from collections import deque
import numpy as np

class logger():

    def __init__(self):
        self.reset()
    
    def log(self, thing):
        self.items.appendleft(np.copy(thing))
    
    def flush(self, filename):
        np.save(filename, np.array(self.items))
    
    def reset(self):
        self.items = deque()