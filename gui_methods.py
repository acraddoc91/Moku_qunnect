import matplotlib.pyplot as plt
import numpy as np
import os

from methods import *
from setup import *

plt.style.use('dark_background')

#|===================|#
#|   HIGHEST LEVEL   |#
#|===================|#

def page_selector(moku=None, wavegen=None):
    form_waves = True
    while True:

        clear_terminal()
        # Get values and save
        per, g_amp, l_amp, r_amp, l_w, r_w, sep, fwhm, g_pos = get_values()
        current_params = {
            'period':per,
            'gaussian amp':g_amp,
            'l square amp':l_amp,
            'r square amp':r_amp,
            'left square width':l_w,
            'right square width':r_w,
            'square separation':sep,
            'gaussian FWHM':fwhm,
            'gaussian position':g_pos
        }
        per = per * 1e-6
        # Convert values to parameters for wave generator
        l_w_param = value_to_parameter(l_w, per)
        r_w_param = value_to_parameter(r_w, per)
        sep_param = value_to_parameter(sep, per)
        fwhm_param = value_to_parameter(fwhm, per)
        g_pos_param = g_pos.split(',')
        g_pos_param = [int(g_pos_param[0]), str(g_pos_param[1]), value_to_parameter(float(g_pos_param[2]), per)]
        
        # Get mean of gaussian from position parameter
        m = gaussian_location(l_w_param, r_w_param, sep_param, g_pos_param[0], g_pos_param[1], g_pos_param[2])

        # Form waves
        if form_waves: 
            g = form_gaussian(m, fwhm_param)
            s = form_square(l_w_param, r_w_param, l_amp, r_amp, sep_param)
        
        # Initialize landing page
        page = landing_page()

        # Page selection
        if page == 'a':
            clear_terminal()
            adjust_parameters(current_params)
            form_waves = True
        
        elif page == 'v':
            wave_visualizer(g, s, per)
            form_waves = False
        
        elif page == 'o':
            upload_waveforms(g, s, moku, wavegen, per, g_amp)
            while True:
                try:
                    moku, wavegen = initialize_moku(SERIAL_NO)
                    break
                except:
                    pass
            form_waves = False

        elif page == 'r':
            reset_parameters()
            form_waves = True
        
        elif page == 'q':
            moku.close()
            clear_terminal()
            break

#|================|#
#|   HIGH LEVEL   |#
#|================|#

def landing_page(msg=''):
    msg = greetings(msg)
    msg = display_params(msg)
    msg = options(msg)
    print(msg)
    selection = input('\nSelect one of the options above: ')
    return selection


def wave_visualizer(g, s, per):
    # converted_data = [value_to_parameter(i, per) for i in DATA]
    for i in range(len(s)):
        if s[i] < 0.0:
            s[i] = 0
    plt.plot(DATA, g, c='violet', linewidth=3)
    plt.plot(DATA, s, c='blue', linewidth=3)
    plt.style.use('dark_background')
    # plt.xticks(np.linspace(-1.0, 1.0, 20))
    plt.show()


def adjust_parameters(curr_params):
    # Initialize "GUI" for parameter adjustment 
    msg = ''
    msg = display_params(msg) + '\n'
    print(msg)
    print('\nEnter values for the following parameters (or ENTER to skip):')
    
    # Start parameter adjustment script
    var_dict = {}
    for v in CONFIG_PARAMS:
        val = input(f'Enter a value for "{v}": ')
        if (val == None) or (val == '') or (val == ' ') or (val == '\n'):
            val = curr_params[v]
        if CONFIG_PARAMS[-1] != v:    
            var_dict[v] = str(val) + '\n'
        else:
            var_dict[v] = str(val)

    # Open file and erase contents
    file = open(CONFIG_PATH, 'r+')
    file.truncate(0)
    # Form content of file
    lines = [var_dict[i] for i in var_dict.keys()]
    file.writelines(lines)
    

# Reset parameters to default value
def reset_parameters():
    file = open(CONFIG_PATH, 'r+')
    file.truncate(0)
    # Form content of file
    lines = ['250\n', '2.0\n', '2.0\n', '5.0\n', '10.0\n', '100\n', '0.53\n', 
             '1,r,0.0']
    file.writelines(lines)


#|===============|#
#|   LOW LEVEL   |#
#|===============|#

def display_params(msg):
    msg += 'Current parameters:'
    values = get_values()
    for i in range(len(values)):
        msg += f'\n  \u2022 {CONFIG_PARAMS[i]}: {values[i]}'
    msg += '\n\nPosition format: \nwave (1/2),position (r/l),offset'
    return msg


def options(msg):
    msg += '\n'
    msg += divider() + '\n'
    for k in OPTIONS_DICT.keys():
        msg += f'\n{k}: {OPTIONS_DICT[k]}'
    
    return msg


def greetings(msg):
    welcome_msg = '\nMOKU SCRIPT\n'
    msg += welcome_msg + '\n'
    msg += divider() + '\n'
    return msg
    

#|==================|#
#|   LOWEST LEVEL   |#
#|==================|#

def clear_terminal():
    os.system('cls')
    return ''


def divider(l=35):
    return '='*(l)