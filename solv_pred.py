import os
import numpy as np
import json

cas_valid_symbol_list = ['0','1','2','3','4','5','6','7','8','9','-'] # '0123456789-'


def load_db(db):
    """
    load database
    """
    current_path = os.getcwd()
    full_db_path = current_path + "\\" + str(db)

    with open(full_db_path) as f:
        db_js = json.load(f)
    #print(db_js[1]["CAS"])

    return db_js

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

def input_cas():
    """
    construct solvent candidate list from user input
    check the format of cas no is valid
    """

    cas_list = []
    i = 0
    to_continue = True

    print("Prepare solvent candidate list. Please submit CAS No. of solvents to be considered as candidates. Add one solvent at one time. Press enter to finish.")

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
                cas_list.append(usr_input_cas_no_spc)
                i += 1
    
    print(cas_list, i)






input_cas()
#load_db("db_mis.json")
