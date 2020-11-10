import numpy as np

SERIAL_NO = '001046'
CONFIG_PATH = 'config.txt'

CONFIG_PARAMS = [
    'period',
    'gaussian amp',
    'l square amp',
    'r square amp',
    'left square width',
    'right square width',
    'square separation',
    'gaussian FWHM',
    'gaussian position'
]

OPTIONS_DICT = {
    'a': 'Adjust parameters',
    'r': 'Reset parameters',
    'v': 'Visualize current waveforms',
    'o': 'Generate output',
    'q': 'Quit'
}

DATA_RANGE = [-10.0, 10.0]
DATA = np.linspace(DATA_RANGE[0], DATA_RANGE[1], 3000)