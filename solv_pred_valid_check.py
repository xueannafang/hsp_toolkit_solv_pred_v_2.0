import solv_pred_reg_txt as sp_rtxt

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

def is_cas_form_valid(input_cas):
    if is_symbol_valid(sp_rtxt.cas_valid_symbol_list, input_cas):
        input_cas_separate = input_cas.split('-')
        if len(input_cas_separate) == 3:
            if '' not in input_cas_separate:
                return True
    return False

def is_symbol_valid(val_sym_list, usr_input):
    no_space_usr_ip = sp_rtxt.rm_spc(usr_input)
    invalid_symbol_exist = False
    for sym in no_space_usr_ip:
        if sym not in val_sym_list:
            invalid_symbol_exist = True
    return not invalid_symbol_exist

def is_option_valid(val_opt_list, usr_input):
    no_space_usr_ip = sp_rtxt.rm_spc(usr_input)
    return no_space_usr_ip in val_opt_list


def is_cas_in(input_cas_list, available_cas_list):
    """
    check if the cas on the current to-be-removed list is on the available cas list
    """
    not_in_list = []

    for input_cas in input_cas_list:
        if input_cas not in available_cas_list:
            not_in_list.append(input_cas)

    return not_in_list