import math
import solv_pred_valid_check as sp_vld_chk

tml_expn_coeff = 0.0007 # thermal expansion coefficient, K^(-1)

def temp_corr_d(ori_d, delta_temp):
    temp_corr_d = float(ori_d) * math.exp(-1.25 * tml_expn_coeff * delta_temp)
    return temp_corr_d

def temp_corr_p(ori_p, delta_temp):
    temp_corr_p = float(ori_p) * math.exp(-0.5 * tml_expn_coeff * delta_temp)
    return temp_corr_p

def temp_corr_h(ori_h, delta_temp):
    temp_corr_h = float(ori_h) * math.exp(-(0.00122 + 0.5 * tml_expn_coeff) * delta_temp)
    return temp_corr_h

def temp_corr_db(db_info_list, current_temp, target_temp):
    delta_temp = target_temp - current_temp
    temp_corr_db_info_list = db_info_list
    not_corr_idx_list = []
    updt_d_list = []
    updt_p_list = []
    updt_h_list = []
 
    for i, entry in enumerate(temp_corr_db_info_list):

        if entry[0] == 'D':
            #check if this entry is a float
            for j, j_old_d in enumerate(entry[1]):

                if sp_vld_chk.is_float(j_old_d):
                    old_d = float(j_old_d)
                    temp_updt_d = temp_corr_d(old_d, delta_temp)
                    updt_d_list.append(temp_updt_d)

                else:
                    err_entry_cas = temp_corr_db_info_list[1][j] #the second list in the full info list correspond to cas
                    err_entry_name = temp_corr_db_info_list[2][j]
                    print('Wrong data type: ' + err_entry_cas + ' ' + err_entry_name + ' \n This solvent will not be considered.')
                    not_corr_idx_list.append(j)
                    updt_d_list.append(j_old_d)
            
            entry[1] = updt_d_list
        
        elif entry[0] == 'P':
            
            for j, j_old_p in enumerate(entry[1]):

                if sp_vld_chk.is_float(j_old_p):
                    old_p = float(j_old_p)
                    temp_updt_p = temp_corr_p(old_p, delta_temp)
                    updt_p_list.append(temp_updt_p)

                else:
                    err_entry_cas = temp_corr_db_info_list[1][j] #the second list in the full info list correspond to cas
                    err_entry_name = temp_corr_db_info_list[2][j]
                    print('Wrong data type: ' + err_entry_cas + ' ' + err_entry_name + ' \n This solvent will not be considered.')
                    not_corr_idx_list.append(j)
                    updt_p_list.append(j_old_p)
                
            entry[1] = updt_p_list
        
        elif entry[0] == 'H':
            #check if this entry is a float
            for j, j_old_h in enumerate(entry[1]):

                if sp_vld_chk.is_float(j_old_h):
                    old_h = float(j_old_h)
                    temp_updt_h = temp_corr_h(old_h, delta_temp)
                    updt_h_list.append(temp_updt_h)

                else:
                    err_entry_cas = temp_corr_db_info_list[1][j] #the second list in the full info list correspond to cas
                    err_entry_name = temp_corr_db_info_list[2][j]
                    print('Wrong data type: ' + err_entry_cas + ' ' + err_entry_name + ' \n This solvent will not be considered.')
                    not_corr_idx_list.append(j)
                    updt_h_list.append(j_old_h)
                
            entry[1] = updt_h_list
    
    not_corr_idx_list_no_rep = sp_vld_chk.rm_repeat(not_corr_idx_list) #solvent idx on this list will be removed from the database for further calculation

    """
    Remove solvents with incomplete info
    """

    temp_corr_db_info_list_filt = sp_vld_chk.rm_incomplete_entry(not_corr_idx_list_no_rep, temp_corr_db_info_list)

    #print(updt_d_list, updt_p_list, updt_h_list)
    print('Temperature correction done.')
    #print('Note: Miscibility check will be disabled for non room temperature setup. \n')
    return temp_corr_db_info_list_filt



def bp_filt_db(db_info_list, bp_low_limit, bp_high_limit = 300):
    """
    Filter solvents whose boiling point is beyond the processable region.
    """
    pass
