from pymoku.instruments import ArbitraryWaveGen
from pymoku import Moku
import numpy as np

from setup import *

# Initializer for Moku device w/ wave generator
def initialize_moku(ser):
    moku = Moku.get_by_serial(ser)
    wavegen = moku.deploy_or_connect(ArbitraryWaveGen)

    return moku, wavegen


def gaussian_location(l_w, r_w, sep, s_wave=1, loc_wave='r', offset=0.0):
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


# Gauss distribution
def gauss(x, std, mean):
    return 1/(std * np.sqrt(2*np.pi))*np.exp(-0.5*((x-mean)/std)**2)

    
# Create gaussian pulse
def form_gaussian(m, fwhm):
    s = fwhm_to_std(fwhm)
    gaussian = []
    for x in DATA:
        if (x < min(DATA)) or (x > max(DATA)):
            gaussian.append(0.0)
        else:
            gaussian.append(gauss(x, std=s, mean=m))
    # gaussian = gaussian / max(gaussian)
    # Sandy Adjustment for AO driver
    gaussian = 2*(gaussian / max(gaussian))-1
    return gaussian


# Create square pulses
def form_square(l_w, r_w, l_a, r_a, sep, def_amp=2.0):
    sq_wave = []
    l_a = l_a / def_amp
    r_a = r_a / def_amp
    for x in DATA:
        # Modified by Sandy for AO
        if ((x <= l_w) and (x >= 0.0)):
            sq_wave.append(l_a)
        elif ((x >= (l_w + sep)) and (x <= (l_w + r_w + sep))):
            sq_wave.append(r_a)
        else:
            # sq_wave.append(0.0)
            sq_wave.append(-1)
    
    return sq_wave


# Get parameters from config file
def get_values():
    values = []
    with open(CONFIG_PATH) as fp: 
        Lines = fp.readlines() 
        for val in Lines:
            val = val.split('\\')[0]
            try:
                values.append(float(val))
            except:
                values.append(val)
    return values


def fwhm_to_std(fwhm):
    return fwhm / 2.355


def value_to_parameter(v, per):
    return v / (450 * per) * 1e-3 * 9.1


def parameter_to_value(p, per):
    return p * 450 * per * 1e+3


# Send waveforms to MOKU for output
def upload_waveforms(gaussian, square, m, i, t, g_amp, s_amp=2.0):
    try:
        i.write_lut(1, gaussian)
        i.write_lut(2, square)

        i.gen_waveform(1, period=t, amplitude=g_amp, interpolation=True, phase=0)
        i.gen_waveform(2, period=t, amplitude=s_amp, interpolation=False, phase=0)

        # Added by Sandy
        i.set_waveform_trigger_output(1,trig_en=True,single=True,duration=t,hold_last=False)
        i.set_waveform_trigger_output(2,trig_en=True,single=True,duration=t,hold_last=False)

        i.set_waveform_trigger(1,source='ext',edge='rising',level=3)
        i.set_waveform_trigger(2,source='ext',edge='rising',level=3)

        i.sync_phase()
    finally:
        m.close()