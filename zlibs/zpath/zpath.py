import os
import sys

LIBRARY_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API_DIR = os.path.join(LIBRARY_DIR, 'zapi')
# sys.path.append(LIBRARY_DIR)
sys.path.append(API_DIR)


class ZPath:
    
    def __init__(self):
        pass
