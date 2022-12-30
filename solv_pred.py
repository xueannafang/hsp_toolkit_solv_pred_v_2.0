import os
import numpy as np
import json

cas_valid_symbol_list = ['0','1','2','3','4','5','6','7','8','9','-'] # '0123456789-'


def load_js(js_file):
    """
    load database
    """
    current_path = os.getcwd()
    full_js_path = current_path + "\\" + str(js_file)

    with open(full_js_path) as f:
        js = json.load(f)
    #print(db_js[1]["CAS"])

    return js

def separate_multi_entry(multi_entry, separate_symbol = ";"):
    """
    separate cells with more than one elements, e.g., immiscible solvent index, synonyms
    """

    multi_entry_list = multi_entry.split(separate_symbol)
    
    return multi_entry_list

def rm_spc(with_spc):
    """
    remove redundant spaces
    """
    no_space = with_spc.replace(' ', '')

    return no_space

def data_available(entry):
    """
    check if the corresponding data is available in the database
    """
    if entry == -1:
        return False

def invalid_input():
    """
    repeat until user press enter to continue
    """
    invalid_check = ' '
    while invalid_check != '':
        invalid_check = input("Invalid input. Press enter to continue. [enter]")

def is_symbol_valid(val_sym_list, usr_input):
    no_space_usr_ip = rm_spc(usr_input)
    invalid_symbol_exist = False
    for sym in no_space_usr_ip:
        if sym not in val_sym_list:
            invalid_symbol_exist = True
    return not invalid_symbol_exist

def is_cas_form_valid(input_cas):
    if is_symbol_valid(cas_valid_symbol_list, input_cas):
        input_cas_separate = input_cas.split('-')
        if len(input_cas_separate) == 3:
            if '' not in input_cas_separate:
                return True
    return False

def is_option_valid(val_opt_list, usr_input):
    no_space_usr_ip = rm_spc(usr_input)
    return no_space_usr_ip in val_opt_list

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
        usr_input_cas_no_spc = rm_spc(usr_input_cas)
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
                invalid_input()
        
        else:
            if not is_cas_form_valid(usr_input_cas):
                print("Wrong CAS No. format")
                invalid_input()
            else:
                usr_cas_list.append(usr_input_cas_no_spc)
                i += 1
    
    #print(usr_cas_list)
    return usr_cas_list

def remove_cas():
    """
    ask user to remove any unwanted solvent cas from the candidate list
    """
    to_continue = True
    cas_to_remove = []

    while to_continue:

        remove_check = input("Do you want to remove any solvent? [y/n] ? ").lower()

        if remove_check in ['y', 'yes']:
            cas_to_remove_usr = input_cas()

        elif remove_check in ['n', 'no']:
            cas_to_remove_usr = []
            to_continue = False

        else:
            invalid_input()
        
        cas_to_remove += cas_to_remove_usr

    if cas_to_remove:
        print('The following solvents will be removed: ')
        print(cas_to_remove)

def generate_candidate_list(default_solv_cand_js):
    """
    Generate solvent candidate list. Ask users to determine whether they want to use default option or manually edit the list.
    """
    print("Generate solvent candidate list: \n You can select to use the default list [1] or manually input the CAS No. [2] \n The default candidate list include the following solvents: ")

    default_solv_candidate_js = load_js(default_solv_cand_js)
    default_solv_candidate_cas_list = []
    default_solv_candidate_name_list = []

    for i, entry in enumerate(default_solv_candidate_js):
        default_solv_candidate_cas_list.append(entry['CAS'])
        default_solv_candidate_name_list.append(entry['Solvent'])
        
    print(default_solv_candidate_js)

    to_continue = True

    while to_continue:

        valid_how_to_select_candidate_list = ['1', '2', 'default', 'manual', 'd', 'm']
        candidate_cas_list = []
        how_to_select_candidate = str(input("Please select the method to construct solvent candidate list. [1-default/2-manual]: " )).lower()

        if not is_option_valid(valid_how_to_select_candidate_list, how_to_select_candidate):
            invalid_input()

        elif how_to_select_candidate in ['1', 'default', 'd']:
            candidate_cas_list = default_solv_candidate_cas_list
            to_continue = False

        elif how_to_select_candidate in ['2', 'manual', 'm']:
            print("Please submit CAS No. of solvents to be considered as candidates. Add one solvent at one time. Press enter to finish.")
            usr_solv_candidate_cas_list = input_cas()
            candidate_cas_list = usr_solv_candidate_cas_list
            to_continue = False
            #print(usr_solv_candidate_cas_list)

    print('You have selected the following solvents as candidates: ')
    print(candidate_cas_list)
        # ask user if there is any solvents to be removed

    remove_cas()
    

def is_cas_in(input_cas_list, available_cas_list):

    not_in_list = []

    for input_cas in input_cas_list:
        if input_cas not in available_cas_list:
            not_in_list.append(input_cas)

    return not_in_list
            


def solv_pred_main(db = 'db_solv_pred_v2.json', candidate = 'default_solv_candidate.json'):



#input_cas()
#load_db("db_mis.json")
#generate_candidate_list('default_solv_candidate.json')