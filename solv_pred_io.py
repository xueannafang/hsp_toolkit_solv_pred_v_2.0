import os
import json
from datetime import datetime
from datetime import date
import numpy as np

import solv_pred_valid_check as sp_vld_chk
import solv_pred_reg_txt as sp_rtxt

today = date.today()
now = datetime.now()

def load_js(js_file):
    """
    load json file
    """
    current_path = os.getcwd()
    full_js_path = current_path + "\\" + str(js_file)

    with open(full_js_path) as f:
        js = json.load(f)
    #print(db_js[1]["CAS"])

    return js

def input_cas():
    """
    construct solvent candidate list from user input
    check the format of cas no is valid
    """

    usr_cas_list = []
    i = 0
    to_continue = True

    while to_continue:

        usr_input_cas = input("Please enter the CAS No. of solvent candidate " + str(i+1) + " : ")
        #print(usr_input_cas)
        usr_input_cas_no_spc = sp_rtxt.rm_spc(usr_input_cas)
        #print(usr_input_cas_no_spc)

        if not usr_input_cas:

            print('Have all the solvent candidates been added?')
            finish_check = continue_check()

            if finish_check== 1:
                to_continue = False

            elif finish_check == 0:
                pass
                # not_finish = ' '
                # while not_finish != '':
                #     not_finish = input("Press enter to continue adding the next solvent. [enter]")

            else:
                sp_vld_chk.invalid_input()
        
        else:
            if not sp_vld_chk.is_cas_form_valid(usr_input_cas):
                print("Wrong CAS No. format")
                sp_vld_chk.invalid_input()
            else:
                usr_cas_list.append(usr_input_cas_no_spc)
                i += 1
    
    #print(usr_cas_list)
    return usr_cas_list


def continue_check():

    continue_check_ip = sp_rtxt.rm_spc(input('[y/n]: ').lower())

    if continue_check_ip in ['y', 'yes']:
        continue_idx = 1
    elif continue_check_ip in ['n', 'no']:
        continue_idx = 0
    else:
        continue_idx = -1
    
    return continue_idx

def get_key(key):
    return lambda x:x.get(key)

def db_init(db_js):
    """
    initialise database
    """
    key_in_db_list = ['No.', 'CAS', 'Name', 'D', 'P', 'H', 'Mole_vol', 'ims_idx', 'bp', 'mw', 'viscosity', 'vis_temp', 'heat_of_vap', 'hov_temp', 'SMILES']

    full_db_info_list = []

    for key in key_in_db_list:
        db_key_list = [key, list(map(get_key(key), db_js))]
        full_db_info_list.append(db_key_list)
    
    return full_db_info_list


def version_info():
    """
    print version info at the beginning of the program
    """

    date_time = get_datetime()
    version_info = 'SolvPredictor v 2.0 \n License: GPL-3.0 \n'
    print(version_info)

    return version_info, date_time


def get_datetime():
    """
    Get current date and time
    """
    
    current_time = now.strftime("%H:%M:%S")
    
    print(str(today) + '  ' + str(current_time))
    
    date_time = [today, now]

    return date_time

def get_datetime_filename():
    """
    generate unique filename based on time and date
    """

    time_date = str(today.strftime("%DD%MM%YY")) + '_' + str(now.strftime("%H%M%S"))

    return time_date


def list2txt(list_to_convert, txt_name):
    current_path = os.getcwd()
    os.mkdir('log')
    full_txt_path = current_path + "\\log\\" + str(txt_name) + '.txt'

    with open(str(full_txt_path), "w") as op_txt:
        op_txt.write(str(list_to_convert))

def calc_log_list2txt(calc_log_list):

    txt_fname = 'calc_log_test'
    list2txt(calc_log_list, txt_fname)


def calc_log_list2js(calc_log_list):
    """
    convert the calc log list to a dictionary
    ready to be converted to json as output
    """

    # cal_log_dict = {}
    calc_log_json_list = []

    js_name = 'calc_log_bsc_chk'

    current_path = os.getcwd()

    if os.path.exists(current_path + '\\log'):
        pass
    else:
        os.mkdir('log')

    full_js_path = current_path + "\\log\\" + str(js_name) + '.json'

    with open(str(full_js_path), "w") as op_js:

        for entry in calc_log_list:

            # cal_log_dict.clear()

            # print('entry: ')
            # print(entry)

            idx = entry[0] #int
            cas_comb = entry[1][0] #list
            conc = np.ndarray.tolist(np.array(entry[1][1]))
            err = np.ndarray.tolist(np.array(entry[1][2]))
            quality = entry[2] # string
            validity = str(entry[-1]) # bool2str
            
            data = {
                'idx' : idx,
                'cas_comb' : cas_comb,
                'conc' : conc,
                'err' : err,
                'quality' : quality,
                'validity' : validity
                }
            
            calc_log_json_list.append(data)
        
        # print(calc_log_json_list)

        json.dump(calc_log_json_list, op_js)

        # jsonStr = json.dump(calc_log_json_list)
    
    # task_name = 'calc_log_bsc_chk'
    # # time_date_name = get_datetime_filename()
    # js_name = task_name

    # list2json(calc_log_json_list, js_name)
    
    return calc_log_json_list
