import solv_pred_reg_txt as sp_rtxt
import solv_pred_io as sp_io

def data_available(entry):
    """
    check if the corresponding data is available in the database
    """
    if entry in [-1, 'None']:
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

def can_be_removed_check(to_be_rm_list, to_rm_from_list):

    cannot_rm_list = is_cas_in(to_be_rm_list, to_rm_from_list)
    #check if cas to be removed is in the candidate list

    if len(cannot_rm_list) != 0:
        print('The following solvents can not be removed and will be ignored:')
        print(cannot_rm_list)
        valid_cas_to_remove = list(set(to_be_rm_list) - set(cannot_rm_list))

    else:
        valid_cas_to_remove = to_be_rm_list
    
    cas_list_after_filt = list(set(to_rm_from_list) - set(valid_cas_to_remove))
    
    return cas_list_after_filt


def finish_check():
    finish_check = sp_io.continue_check()

    if finish_check == 1:
        to_continue = False

    elif finish_check == 0:
        pass

    else:
        invalid_input()
    
    return to_continue


def not_in_db_filt(before_filt_list, not_in_db_list):
    """
    raise warning and remove not-in-db candidates
    """
    if len(not_in_db_list) != 0:
        after_db_filt_cand_list = list(set(before_filt_list) - set(not_in_db_list))
        print('Done. \n The following solvents are not in the database and will be ignored: ')
        print(not_in_db_list)
    else:
        after_db_filt_cand_list = before_filt_list
    
    return after_db_filt_cand_list


def is_float(usr_input_number_str):
    """
    Check if usr input is a float
    """
    try:
        float(usr_input_number_str)
        return True

    except ValueError:
        return False

def rm_repeat(old_list):
    """
    Remove repeated elements in the list
    """

    no_repeat_set = set(old_list)
    new_list = list(no_repeat_set)

    return new_list

def descend_list(random_list):
    """
    descend all the elements in a list
    """
    sort_descend_list = list.sort(random_list, reverse = True)

    return sort_descend_list


def rm_incomplete_entry(to_rm_idx_list, to_rm_from_db_info_list):
    """
    remove unwanted idx from current db info list
    """
    descend_idx_list = descend_list(to_rm_idx_list)

    after_rm_db_info_list = to_rm_from_db_info_list

    for i, entry in after_rm_db_info_list:
        new_db_info_list = entry[1]
        for a, j in enumerate(descend_idx_list):
            new_db_info_list.pop(j)
        entry[1] = new_db_info_list
    
    return after_rm_db_info_list
    
    
    







