from __future__ import print_function

import matplotlib.pyplot as plt
import numpy as np
import time
import sys
import os

# Custom libraeies
from gui_methods import *
from methods import *
from setup import *

import sys
from time import sleep

print('Connecting to Moku...')
while True:
    try:
        moku, wavegen = initialize_moku(SERIAL_NO)
        break
    except:
        print('Connection attempt failed. Retrying')
clear_terminal()
page_selector(moku, wavegen)