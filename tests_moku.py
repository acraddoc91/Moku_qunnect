import numpy as np
from gui_methods import *
from methods import *
from setup import *

# l_w = 0.4
# r_w = 0.2
# sep = 0.2
# fwhm = 0.2355

g_loc = [1, 'r', 0.0]
l_w = 0.18
r_w = 0.09
sep = 0.03
fwhm = 0.53

period = 5e-6
g_amp = 0.8
s_amp = 2.0

def val_to_param(val, per=period):
    return val / (450*per) * 1e-3

l_w = val_to_param(l_w)
r_w = val_to_param(r_w)
sep = val_to_param(sep)
fwhm = val_to_param(fwhm)

def gaussian_location(s_wave=1, loc_wave='r', offset=0.0):
    global l_w
    global r_w
    global sep

    if s_wave == 1:
        if loc_wave == 'l':
            return 0.0 + offset
        elif loc_wave == 'r':
            return l_w + offset
    elif s_wave == 2:
        if loc_wave == 'l':
            return l_w + sep + offset
        if loc_wave == 'r':
            return l_w + sep + r_w + offset 

m = gaussian_location(g_loc[0], g_loc[1], g_loc[2])


moku, wavegen = initialize_moku(ser=SERIAL_NO)

g = form_gaussian(m, fwhm)
s = form_square(l_w, r_w, sep)

upload_waveforms(g, s, moku, wavegen, t=period)