import os
import json

import solv_pred_valid_check as sp_vld_chk
import solv_pred_reg_txt as sp_rtxt


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
                not_finish = ' '
                while not_finish != '':
                    not_finish = input("Press enter to continue adding the next solvent. [enter]")

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

    continue_check_ip = input('[y/n]: ').lower()

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