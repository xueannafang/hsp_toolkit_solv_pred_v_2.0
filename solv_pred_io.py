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

            finish_check = input("Have all the solvent candidates been added? [y/n] ? ").lower()

            if finish_check in ['y', 'yes']:
                to_continue = False

            elif finish_check in ['n', 'no']:
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