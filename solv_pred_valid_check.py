import numpy as np
from scipy.linalg import pinv

import solv_pred_reg_txt as sp_rtxt
import solv_pred_io as sp_io
import solv_pred_fetch_info as sp_ftch_info

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
    to_continue_finish_chk = True

    if finish_check == 1:
        to_continue_finish_chk = False

    elif finish_check == 0:

        pass

    else:
        invalid_input()
    
    return to_continue_finish_chk


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

def is_n_vld(usr_input_n):
    """
    check if the usr input is a positive integer larger or equal to 2
    """
    try:
        if int(usr_input_n) > 1:
            return True
        elif int(usr_input_n) <= 1:
            print('Invalid input of n: n must be >= 2')
            return False
    
    except ValueError:
        print('Invalid input of n: Please enter an integer >= 2')
        return False


def is_tol_err_vld(usr_input_tol_err):
    """
    check if the usr input tol_err is a positive float
    """
    try:
        if float(usr_input_tol_err) > 0:
            return True
        
        elif float(usr_input_tol_err) <= 0:
            print('Invalid input of tol_err: tolerance of error must be a positive float')
            return False
    
    except ValueError:
        print('Invalid input of tol_err: Please enter a positive float')
        return False


def is_tgt_vld(usr_input_tgt):
    """
    check if the usr input tgt is a non-negative float
    """
    try:
        if float(usr_input_tgt) >= 0:
            return True
        
        elif float(usr_input_tgt) < 0:
            print('Invalid input of target HSP: Must be a non-negative float')
            return False
    
    except ValueError:
        print('Invalid input of target HSP: Must be a non-negative float')
        return False

def is_tol_conc_vld(usr_input_tol_conc):
    """
    check if the usr input tol_conc is a positive float between 0 and 1
    """
    try:
        if float(usr_input_tol_conc) >= 0 and float(usr_input_tol_conc) <= 1:
            return True
        
        elif float(usr_input_tol_conc) < 0 or float(usr_input_tol_conc) > 1:
            print('Invalid tol_conc: tolerance of concentration must be a float between 0 and 1')
            return False
    
    except ValueError:
        print('Invalid input of tol_conc: Please enter a float between 0 and 1')
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
    if len(to_rm_idx_list) != 0:

        descend_idx_list = descend_list(to_rm_idx_list)

        after_rm_db_info_list = to_rm_from_db_info_list

        for i, entry in after_rm_db_info_list:
            new_db_info_list = entry[1]
            for a, j in enumerate(descend_idx_list):
                new_db_info_list.pop(j)
            entry[1] = new_db_info_list
    
    else:

        after_rm_db_info_list = to_rm_from_db_info_list
        
    
    return after_rm_db_info_list


def is_cand_list_longer_than_n(cand_cas_list, n):
    """
    validate if the candidate list is longer than user-specified n
    """
    if len(cand_cas_list) > int(n):
        print('Validation of n is done.')
        return True
    else:
        print('Warning: Candidate list does not contain enough solvents to iterate through.')
        print('Please add more solvent candidates or decrease n.')
        return False


def is_target_achievable(db_info_list, cand_cas_list, target_hsp):
    """
    validate if the target is covered by the region connected by all the solvent candidate in the hansen space
    """
    cand_idx_cas_hsp_list = sp_ftch_info.fetch_idx_cas_hsp(cand_cas_list, db_info_list)

    all_d = sp_ftch_info.fetch_sub_hsp(cand_idx_cas_hsp_list, 'd')
    all_p = sp_ftch_info.fetch_sub_hsp(cand_idx_cas_hsp_list, 'p')
    all_h = sp_ftch_info.fetch_sub_hsp(cand_idx_cas_hsp_list, 'h')

    d_range = [min(all_d), max(all_d)]
    p_range = [min(all_p), max(all_p)]
    h_range = [min(all_h), max(all_h)]

    target_d = float(target_hsp[0])
    target_p = float(target_hsp[1])
    target_h = float(target_hsp[2])

    if target_d > d_range[0] and target_d < d_range[1]:
        print('Target D validation done.')
        d_check = True
    else:
        print('Target D is not achievable.')
        print('Target D must be in the interval of ' + str(d_range[0]) + ' to ' + str(d_range[1]))
        d_check = False
    
    if target_p > p_range[0] and target_p < p_range[1]:
        print('Target P validation done.')
        p_check = True
    else:
        print('Target P is not achievable.')
        print('Target P must be in the interval of ' + str(p_range[0]) + ' to ' + str(p_range[1]))
        p_check = False
    
    if target_h > h_range[0] and target_h < h_range[1]:
        print('Target H validation done.')
        h_check = True
    else:
        print('Target H is not achievable.')
        print('Target H must be in the interval of ' + str(h_range[0]) + ' to ' + str(h_range[1]))
        h_check = False
    
    if False in [d_check, p_check, h_check]:
        target_check = False
    
    else:
        target_check = True

    return target_check

    
def is_c_stable(c_std, c_tot, tol_rep_std = 0.1):
    """
    check if the standard deviation along all the perturbation is below tol_rep_std (default = 0.1)
    check if the total mean concentration is above 105% or below 95%
    """

    stat_check_c = True

    if c_std > tol_rep_std or c_tot > 1.05 or c_tot < 0.95:

        stat_check_c = False
    
    return stat_check_c

def is_err_mat_accptbl(e_mean_ov_t_arr, tol_err_list):
    """
    check if the error is acceptable
    """

    flt_tol_err_list = list(np.float_(tol_err_list))

    err_mat_check = True

    if abs(e_mean_ov_t_arr[0][0]) > flt_tol_err_list[0] or abs(e_mean_ov_t_arr[1][0]) > flt_tol_err_list[1] or abs(e_mean_ov_t_arr[2][0]) > flt_tol_err_list[2]:

        err_mat_check = False
    
    return err_mat_check

    




    
    
    







