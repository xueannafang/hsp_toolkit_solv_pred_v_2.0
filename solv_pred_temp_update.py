"""
solv_pred_temp_update includes functions for user-personalised temperautre set up and correction for HSP.
"""

import math
import solv_pred_valid_check as sp_vld_chk

tml_expn_coeff = 0.0007 # thermal expansion coefficient, unit K^(-1), ref: HSPiP website

def temp_corr_d(ori_d: float, delta_temp: float) -> float:
    """return temp-corrected d

    Args:
        ori_d (float): d before temp corr
        delta_temp (float): temperature difference from current

    Returns:
        float: temp-corrected d
    """
    temp_corr_d = float(ori_d) * math.exp(-1.25 * tml_expn_coeff * delta_temp)

    return temp_corr_d

def temp_corr_p(ori_p: float, delta_temp: float) -> float:
    """return temp-corrected p

    Args:
        ori_p (float): p before temp corr
        delta_temp (float): temperature difference from current

    Returns:
        float: temp-corrected p
    """

    temp_corr_p = float(ori_p) * math.exp(-0.5 * tml_expn_coeff * delta_temp)

    return temp_corr_p

def temp_corr_h(ori_h: float, delta_temp: float) -> float:
    """return temp-corrected h

    Args:
        ori_h (float): h before temp corr
        delta_temp (float): temperature difference from current

    Returns:
        float: temp-corrected h
    """
    temp_corr_h = float(ori_h) * math.exp(-(0.00122 + 0.5 * tml_expn_coeff) * delta_temp)
    
    return temp_corr_h

def temp_corr_db(db_info_list: list, current_temp: float, target_temp: float) -> list:
    """return database info list with temperature-corrected HSP.

    Args:
        db_info_list (list): db before HSP temperature correction.
        current_temp (float): current temp in degree c.
        target_temp (float): target temp in degree c.

    Returns:
        list: db info after HSP temperature correction.
    """

    delta_temp = target_temp - current_temp

    temp_corr_db_info_list = db_info_list

    # not_corr_idx_list = [] # list of idx that temp-correction will not be applied due to data missing or wrong data type

    updt_d_list = []
    updt_p_list = []
    updt_h_list = []
 
    for i, entry in enumerate(temp_corr_db_info_list):
        
        # entry[0] is sub HSP type
        # entry[1] is all the data of corresponding sub HSP

        if entry[0] == 'D':

            # check if this entry is a float

            for j, j_old_d in enumerate(entry[1]):

                if sp_vld_chk.is_float(j_old_d):

                    old_d = float(j_old_d)
                    temp_updt_d = temp_corr_d(old_d, delta_temp)
                    updt_d_list.append(temp_updt_d)

                # else:

                #     # data missing or wrong data type

                #     err_entry_cas = temp_corr_db_info_list[1][j] # record the cas of error item
                #     err_entry_name = temp_corr_db_info_list[2][j] # record the name of error item

                #     print('Wrong data type or data missing for D: \n' + err_entry_cas + ' ' + err_entry_name + ' \n This solvent will not be considered.')

                #     not_corr_idx_list.append(j)
                #     updt_d_list.append(j_old_d)
            
            entry[1] = updt_d_list
        
        elif entry[0] == 'P':
            
            for j, j_old_p in enumerate(entry[1]):

                if sp_vld_chk.is_float(j_old_p):

                    old_p = float(j_old_p)
                    temp_updt_p = temp_corr_p(old_p, delta_temp)
                    updt_p_list.append(temp_updt_p)

                # else:
                    
                #     err_entry_cas = temp_corr_db_info_list[1][j]
                #     err_entry_name = temp_corr_db_info_list[2][j]
                #     print('Wrong data type or data missing for P: ' + err_entry_cas + ' ' + err_entry_name + ' \n This solvent will not be considered.')
                #     not_corr_idx_list.append(j)
                #     updt_p_list.append(j_old_p)
                
            entry[1] = updt_p_list
        
        elif entry[0] == 'H':
            
            for j, j_old_h in enumerate(entry[1]):

                if sp_vld_chk.is_float(j_old_h):

                    old_h = float(j_old_h)
                    temp_updt_h = temp_corr_h(old_h, delta_temp)
                    updt_h_list.append(temp_updt_h)

                # else:

                #     err_entry_cas = temp_corr_db_info_list[1][j] #the second list in the full info list correspond to cas
                #     err_entry_name = temp_corr_db_info_list[2][j]
                #     print('Wrong data type or data missing for H: ' + err_entry_cas + ' ' + err_entry_name + ' \n This solvent will not be considered.')

                #     not_corr_idx_list.append(j)
                #     updt_h_list.append(j_old_h)
                
            entry[1] = updt_h_list
    
    # not_corr_idx_list_no_rep = sp_vld_chk.rm_repeat(not_corr_idx_list) # remove repeated idx. solvent idx on this list will be removed from the database for further calculation

    # temp_corr_db_info_list_filt = sp_vld_chk.rm_incomplete_entry(not_corr_idx_list_no_rep, temp_corr_db_info_list) # Remove solvents with incomplete info

    return temp_corr_db_info_list

    # return temp_corr_db_info_list_filt