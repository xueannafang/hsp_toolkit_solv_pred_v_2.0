"""
solv_pred_valid_check includes functions to validate a specific variable.
"""

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
    """repeat until user press enter to continue
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

def is_option_valid(val_opt_list: list, usr_input: str) -> bool:
    """check if the usr input is within valid options list.

    Args:
        val_opt_list (list): a list. containing all the possible valid usr input.
        usr_input (str): already in lower cased input, but may include space.

    Returns:
        bool: if usr input is valid, return True. Else return False.
    """
    no_space_usr_ip = sp_rtxt.rm_spc(usr_input) # remove any space in usr input

    return no_space_usr_ip in val_opt_list

def is_cas_in(input_cas_list: list, available_cas_list: list) -> list:
    """return a list of cas that is not on the current available list.

    Args:
        input_cas_list (list): cas list to check
        available_cas_list (list): cas list avilable

    Returns:
        list: cas not avilable
    """
    not_in_list = []

    for input_cas in input_cas_list:

        if input_cas not in available_cas_list:

            not_in_list.append(input_cas)

    return not_in_list

def can_be_removed_check(to_be_rm_list: list, to_rm_from_list: list) -> list:
    """return cas list that removes valid entries in to_be_rm_list from to_rm_from_list.

    Args:
        to_be_rm_list (list): usr generated cas list to be removed.
        to_rm_from_list (list): usr generated cas list before the removing step.

    Returns:
        list: after removing valid usr-specified to-be-removed cas.
    """

    cannot_rm_list = is_cas_in(to_be_rm_list, to_rm_from_list) # cas list that is not avilable on the current list

    if len(cannot_rm_list) != 0:

        print('The following solvents are absent from current candidate list and will be ignored:')
        print(cannot_rm_list)

        valid_cas_to_remove = list(set(to_be_rm_list) - set(cannot_rm_list)) # list of cas that can be removed

    else:

        valid_cas_to_remove = to_be_rm_list
    
    cas_list_after_filt = list(set(to_rm_from_list) - set(valid_cas_to_remove)) # remove requested cas from current candidate list
    
    return cas_list_after_filt


def finish_check() -> bool:
    """return bool to determine finish or not.

    Returns:
        bool: True for not exit. False for exit.
    """

    finish_check = sp_io.continue_check()

    to_continue_finish_chk = True

    if finish_check == 1: # to finish
        to_continue_finish_chk = False

    elif finish_check == 0: # not to finish

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


def is_float(usr_input_number_str: str) -> bool:
    """return bool of whether usr input is a float.

    Args:
        usr_input_number_str (str): usr input number after removing space

    Returns:
        bool: True if is float; False if else.
    """
    try:
        float(usr_input_number_str)
        return True

    except ValueError:
        return False

def is_n_vld(usr_input_n: str) -> bool:
    """return bool of whether the usr input is a positive integer larger or equal to 2.

    Args:
        usr_input_n (str): input n.

    Returns:
        bool: True if n is an int >= 2; else False.
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


def is_tol_err_vld(usr_input_tol_err: str) -> bool:
    """return bool of whether the usr input tol_err is a positive float.

    Args:
        usr_input_tol_err (str): input toloerance of error for d, p, h.

    Returns:
        bool: True if input tol_err is a positive float; else False.
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

def is_tgt_fmt_vld(usr_input_tgt: str) -> bool:
    """return bool of whether the usr input target HSP is a positive float.

    Args:
        usr_input_tgt (str): input target HSP for d, p, h.

    Returns:
        bool: True if input target HSP is a positive float; else False.
    """
    try:

        if float(usr_input_tgt) > 0:

            return True
        
        elif float(usr_input_tgt) <= 0:

            print('Invalid input of target HSP: Must be a positive float')

            return False
    
    except ValueError:

        print('Invalid input of target HSP: Please enter a positive float')

        return False

def is_tgt_vld(usr_input_tgt: str) -> bool:
    """return bool of whether usr_input_tgt is a non-negative float.

    Args:
        usr_input_tgt (str): input target d, p, h.

    Returns:
        bool: True if input target HSP is a non-negative float; else False.
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

def is_tol_conc_vld(usr_input_tol_conc: str) -> bool:
    """return bool of whether the usr input tol_conc is a positive float between 0 and 1.

    Args:
        usr_input_tol_conc (str): input tolerance of concentration.

    Returns:
        bool: True if input is a float between 0 and 1; else False.
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


def rm_repeat(old_list: list) -> list:
    """return list without repeated entries

    Args:
        old_list (list): list that may include repeated entries

    Returns:
        list: without repeated entries
    """

    no_repeat_set = set(old_list) # remove repeated terms
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


def is_cand_list_longer_than_n(cand_cas_list: list, n: int) -> bool:
    """return bool to validate if the candidate list is longer than user-specified n.

    Args:
        cand_cas_list (list): candidate cas list.
        n (int): max number of solvents in each combination.

    Returns:
        bool: True if cand_cas_list is longer than n; else False.
    """
    if len(cand_cas_list) > int(n):

        print('Validation of n is done.')

        return True

    else:

        print('Warning: Candidate list does not contain enough solvents to iterate through.')

        print('Please add more solvent candidates or decrease n.')

        return False


def is_target_achievable(db_info_list: list, cand_cas_list: list, target_hsp: list) -> bool:
    """return bool that validates if the target is covered by the region connected by all the solvent candidate in the hansen space.

    Args:
        db_info_list (list): list with full db info
        cand_cas_list (list): all candidate cas
        target_hsp (list): target d, p, h.

    Returns:
        bool: True if target hsp is located in the region connected by all the candidates in the Hansen space; else False.
    """
    cand_idx_cas_hsp_list = sp_ftch_info.fetch_idx_cas_hsp(cand_cas_list, db_info_list) # fetch hsp from full db info list

    all_d = sp_ftch_info.fetch_sub_hsp(cand_idx_cas_hsp_list, 'd')
    all_p = sp_ftch_info.fetch_sub_hsp(cand_idx_cas_hsp_list, 'p')
    all_h = sp_ftch_info.fetch_sub_hsp(cand_idx_cas_hsp_list, 'h')

    # calculate the range of candidate-covered region in the Hansen space

    d_range = [min(all_d), max(all_d)]
    p_range = [min(all_p), max(all_p)]
    h_range = [min(all_h), max(all_h)]

    target_d = float(target_hsp[0])
    target_p = float(target_hsp[1])
    target_h = float(target_hsp[2])

    # check if the target is within this region

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

    
def is_c_stable(c_std_vec, tol_rep_std = 0.1):
    """
    check if the standard deviation along all the perturbation is below tol_rep_std (default = 0.1)
    check if the total mean concentration is above 105% or below 95%
    """

    stat_check_c = True

    for c_std in c_std_vec:
        if c_std > tol_rep_std:
            stat_check_c = False

    
    return stat_check_c


def is_c_vld(c_mean_vec):
    """
    check if total conc is between 0.95 and 1.05
    check if each c_mean is positive
    """

    c_tot = sum(c_mean_vec)
    vld_check_c = True

    for c_mean in c_mean_vec:
        
        if c_mean < 0 or c_mean > 1:
            vld_check_c = False

    if c_tot > 1.1 or c_tot < 0.9:
        vld_check_c = False
    
    return vld_check_c


def is_err_mat_accptbl(e_mean_arr, tol_err_list):
    """
    check if the error is acceptable
    """

    flt_tol_err_list = list(np.float_(tol_err_list))

    e_d = e_mean_arr[0]
    e_p = e_mean_arr[1]
    e_h = e_mean_arr[2]

    tol_e_d, tol_e_p, tol_e_h = flt_tol_err_list

    err_mat_check = True

    if abs(e_d) > tol_e_d or abs(e_p) > tol_e_p or abs(e_h) > tol_e_h:

        err_mat_check = False
    
    return err_mat_check

def is_conc_above_tol(c_mean_vec, tol_conc):
    """
    check if each entry is above the concentration threshold
    save all the validity of each candidate with its idx in c_mean_vec
    """
    
    # print('conc_fil: ')
    # print(c_mean_vec)
    # print('tol_conc: ')
    # print(tol_conc)

    conc_tol_check_log = []

    for solv_idx, c_mean in enumerate(c_mean_vec):

        if c_mean[0] < tol_conc:

            conc_tol_check_log.append([solv_idx, False])
        
        else:
            conc_tol_check_log.append([solv_idx, True])
    
    # print('c_mean[0]: ')
    # print(c_mean[0])
    # print('conc_tol_chk_log: ')
    # print(conc_tol_check_log)

    return conc_tol_check_log


def is_vld_comb_exist(vld_comb_n):
    """
    check if there is any vld results
    """
    is_vld_comb_exist == True

    if vld_comb_n == 0:
        print('Warning: No valid results. \n \nYou may need to: \n - Edit candidates \n - Increase tolerance of error \n - Modify target')
        is_vld_comb_exist == False
    
    return is_vld_comb_exist
        

def bp_chk(vld_comb_list, tgt_temp):
    """
    check if the bp of any predicted solvent is below the set temperature

    add bp_quality, bp_validity as new keys
    """
    for each_solv_dict in vld_comb_list:

        bp = each_solv_dict['bp']
        if bp in [None, -1]:
            each_solv_dict['bp_chk_msg'] = 'NA'
            each_solv_dict['bp_validity'] = 'NA'
        else:
            if bp < tgt_temp:
                each_solv_dict['bp_chk_msg'] = 'Below set temp'
                each_solv_dict['bp_validity'] = False
            else:
                each_solv_dict['bp_chk_msg'] = 'Above or equal to set temp'
                each_solv_dict['bp_validity'] = True
    
    bp_chk_vld_list = vld_comb_list

    return bp_chk_vld_list


def ims_chk(vld_comb_list):
    """
    check if any solvent is immiscible with others in the group

    note that in this version, immiscibility is only based on data available on PubChem

    Some data did not specific measured temperature, so this result is just for a reference
    """
    idx_list = []
    ims_idx_list = []

    for each_solv_dict in vld_comb_list:

        if each_solv_dict['ims_idx'] == None:

            each_solv_dict['ims_chk_msg'] = 'No recorded miscibility issue or no solubility record. Manual check is recommended.'
            each_solv_dict['ims_solvent_in_comb'] = None
            each_solv_dict['ims_validity'] = 'NA'

        else:
            idx_list.append(each_solv_dict['No.'])
            ims_idx_reg_list = sp_rtxt.separate_multi_entry(each_solv_dict['ims_idx'], ';')
            ims_idx_list.append(ims_idx_reg_list)
    
    all_ims_comb_list = []

    for i, idx in enumerate(idx_list):
        for j, ims_idx in enumerate(ims_idx_list):
            if i == j:
                pass
            elif i != j:
                if idx in ims_idx_list[j]:
                    all_ims_comb_list.append([idx, ims_idx])
    
   
    for each_solv_dict in vld_comb_list:

        if 'ims_validity' in each_solv_dict.keys():
            pass

        else:

            if len(all_ims_comb_list) == 0:

                each_solv_dict['ims_chk_msg'] = 'No recorded miscibility issue. Manual check is recommended if temperature has been varied.'
                each_solv_dict['ims_solvent_in_comb'] = None
                each_solv_dict['ims_validity'] = True

            else:

                ims_solv_in_comb_list = []

                for k, ims_comb in enumerate(all_ims_comb_list):

                    if each_solv_dict['idx'] == ims_comb[0]:

                        ims_solv_in_comb_list.append(ims_comb[1])
                        
                        each_solv_dict['ims_chk_msg'] = 'May cause immiscible issue.'
                        each_solv_dict['ims_solvent_in_comb'] = ims_solv_in_comb_list
                        each_solv_dict['ims_validity'] = False

    
    ims_chk_vld_list = vld_comb_list

    return ims_chk_vld_list





        

        
    
                    










    




    
    
    







