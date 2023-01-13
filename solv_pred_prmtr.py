"""
solv_pred_prmtr includes functions for user-personalised calculation and basic filtration parameters, i.e., n, target HSP, acceptable error for calculated HSP and lowest acceptable concentration for predicted solvents. 
"""

import solv_pred_valid_check as sp_vld_chk
import solv_pred_io as sp_io
import solv_pred_temp_update as sp_temp_updt
import solv_pred_reg_txt as sp_rtxt
import solv_pred_cand_edit as sp_ed


def specify_temp(orig_db_info_list: list) -> list:
    """Return temperature-corrected db based on updated HSP, whether temperature has been updated, target temperature in degree c.

    Args:
        orig_db_info_list (list): db with HSP before temperature correction.

    Returns:
        list: [db info list with temp-updated HSP, temp_edit (idx to show if temp has been modified: 0 - unmodified; 1 - modified), target_temp (unit in degree c)].
    """
    
    to_continue_spf_temp = True
    default_temp = 25 # default temp in degree c
    target_temp = default_temp

    # user interactive process to specify temp and correct HSP
    
    while to_continue_spf_temp:

        valid_temp_confirm_list = ['t', 'c', 'continue', 'q', 'quit']
        temp_confirm = input('[t] - set a different temperature \n[c] - continue as room temperature (25 degree c). \n[q] - quit\n').lower()

        temp_edit = 0

        if not sp_vld_chk.is_option_valid(valid_temp_confirm_list, temp_confirm):

            sp_vld_chk.invalid_input()

        elif temp_confirm in ['t']: # update temp
            
            usr_target_temp = sp_rtxt.rm_spc(input('Please enter the target temperature (in degree C): '))
            usr_target_temp_is_float = sp_vld_chk.is_float(usr_target_temp) # check this is a float

            if usr_target_temp_is_float is False:

                sp_vld_chk.invalid_input()
                print('Please enter a valid number.')
            
            else:

                target_temp = float(usr_target_temp)
                
                if target_temp == default_temp: # unchanged temp

                    print('25 C is the default temperature. \n Temperature correction will not be applied.')
                    db_temp_corr = orig_db_info_list
                    
                    print('Continue?')
                    to_continue_spf_temp = sp_vld_chk.finish_check()
                    
                
                else: # invoke temp correction
                    
                    print('Temperature has been set as: ' + usr_target_temp)

                    print('Applying temperature correction for standard HSP...')

                    db_temp_corr = sp_temp_updt.temp_corr_db(orig_db_info_list, 25, target_temp)

                    print('Database HSP temperature correction done.')

                    temp_edit = 1 # indicating temp has been updated
                    
                    to_continue_spf_temp = False

        elif temp_confirm in ['c', 'continue']:
            
            db_temp_corr = orig_db_info_list # pass the unmodified db to the next step
            to_continue_spf_temp = False
        
        elif temp_confirm in ['q', 'quit']:

            print('Confirm to quit?')
            to_finish_temp_confm = sp_vld_chk.finish_check()

            if to_finish_temp_confm is not True:

                exit()
    
    return [db_temp_corr, temp_edit, target_temp]


def specify_cand_parameter() -> list:
    """return usr-specified calculation parameters or default parameters.

    Returns:
        list: usr-specified or default calc parameter - [n, tol_err_d, tol_err_p, tol_err_h, tol_conc].
    """
    
    usr_cand_parameter_default_list = [2, 0.5, 0.5, 0.5, 0.01] # [n, tol_err_d, tol_err_p, tol_err_h, tol_conc]

    # check if usr wants to use default or not

    usr_cand_parameter_list = []

    to_continue_spf_cand_prmt = True

    while to_continue_spf_cand_prmt:

        usr_set_option = input('Set parameters: \n[d] - use default settings for all parameters. \n[m] - manually set parameters. \n')

        valid_set_option_list = ['d', 'm', 'default', 'manual']

        usr_cand_parameter_list = []

        if not sp_vld_chk.is_option_valid(valid_set_option_list, usr_set_option):

            sp_vld_chk.invalid_input()
        
        elif usr_set_option in ['d', 'default']:

            usr_cand_parameter_list = usr_cand_parameter_default_list
            print('Default parameters will be applied.')
            print('[n, tol_err_d, tol_err_p, tol_err_h, tol_conc] : ' + str(usr_cand_parameter_default_list))

            print('Continue?')
            to_continue_spf_cand_prmt = sp_vld_chk.finish_check()
        
        elif usr_set_option in ['m', 'manual']:

            print('Please specify parameters:')
            
            print('n is the maximum number of solvents involved in each prediction.\nMust be a postivie integer >= 2. (recommend to be 2 or 3) ')

            usr_n = sp_rtxt.rm_spc(input('Please specify n: '))
            
            print('tolerance of error is the highest acceptable absolute error of HSP from the predicted solvent mixture. \n Must be a positive float.')

            usr_tol_err_d = sp_rtxt.rm_spc(input('Please specify tolerance of error for dispersion term (tol_err_D): '))

            usr_tol_err_p = sp_rtxt.rm_spc(input('Please specify tolerance of error for dipolar term (tol_err_P): '))

            usr_tol_err_h = sp_rtxt.rm_spc(input('Please specify tolerance of error for hydrogen bond term (tol_err_H): '))
            
            print('lowest acceptable concentration is the threshold of predicted solvent concentration below which will be filtered out. \nMust be a float between 0 and 1. \n')

            usr_tol_conc = sp_rtxt.rm_spc(input('Please specify lowest acceptable concentration: '))

            # validate the format of each parameter

            usr_n_valid = sp_vld_chk.is_n_vld(usr_n)
            usr_tol_err_d_valid = sp_vld_chk.is_tol_err_vld(usr_tol_err_d)
            usr_tol_err_p_valid = sp_vld_chk.is_tol_err_vld(usr_tol_err_p)
            usr_tol_err_h_valid = sp_vld_chk.is_tol_err_vld(usr_tol_err_h)
            usr_tol_conc_valid = sp_vld_chk.is_tol_conc_vld(usr_tol_conc)

            parameter_valid_check_list = [usr_n_valid, usr_tol_err_d_valid, usr_tol_err_p_valid, usr_tol_err_h_valid, usr_tol_conc_valid] # list of bool values whehter each parameter is valid or not
            
            if False not in parameter_valid_check_list:  # all

                usr_cand_parameter_list = [int(usr_n), float(usr_tol_err_d), float(usr_tol_err_p), float(usr_tol_err_h), float(usr_tol_conc)]

                print('n, tol_err, tol_conc have been specified as: ')
                print(usr_cand_parameter_list)

                print('Continue?')
                to_continue_spf_cand_prmt = sp_vld_chk.finish_check()
            
    return usr_cand_parameter_list


def specify_n() -> int:
    """return usr-specified n

    Returns:
        int: usr-specified n
    """
    
    to_continue_spf_n = True
    while to_continue_spf_n:

        print('n is the maximum number of solvents involved in each prediction.\nMust be a postivie integer >= 2. (recommend to be 2 or 3) ')

        usr_n = sp_rtxt.rm_spc(input('Please specify n: '))
        usr_n_valid = sp_vld_chk.is_n_vld(usr_n)
        
        if usr_n_valid is True:

            print('n has been specified as: ')
            print(usr_n)
            print('Continue?')
            to_continue_spf_n = sp_vld_chk.finish_check()
            usr_n = int(usr_n)
    
    return usr_n

def specify_target() -> list:
    """return usr-specified target HSP.

    Returns:
        list: [target_d, target_p, target_h]
    """

    usr_tgt_hsp_list = []
    to_continue_spf_tgt = True

    while to_continue_spf_tgt:

        print('target d, p, h are target HSPs to be achieved. \n Must be non-negative float.')
        usr_tgt_d = sp_rtxt.rm_spc(input('Please specify the target of dispersion term (target D): '))
        usr_tgt_p = sp_rtxt.rm_spc(input('Please specify the target of dipolar term (target P): '))
        usr_tgt_h = sp_rtxt.rm_spc(input('Please specify the target of hydrogen bond term (target H): '))

        # format checking - rough validate

        usr_tgt_d_valid = sp_vld_chk.is_tgt_fmt_vld(usr_tgt_d)
        usr_tgt_p_valid = sp_vld_chk.is_tgt_fmt_vld(usr_tgt_p)
        usr_tgt_h_valid = sp_vld_chk.is_tgt_fmt_vld(usr_tgt_h)

        parameter_valid_check_list = [usr_tgt_d_valid, usr_tgt_p_valid, usr_tgt_h_valid]
            
        if False not in parameter_valid_check_list:  # all

            usr_tgt_hsp_list = [usr_tgt_d, usr_tgt_p, usr_tgt_h]
            print('target d, target p, target h have been specified as: ')

            print(usr_tgt_hsp_list)
            print('Continue?')
            to_continue_spf_tgt = sp_vld_chk.finish_check()

    return usr_tgt_hsp_list


def get_parameter(cand_cas_list: list, db_info_list: list) -> list:
    """return validated usr-specified parameters for calculation.

    Args:
        cand_cas_list (list): candidate cas list.
        db_info_list (list): db info.
    
    Returns:
        list: [vld_usr_n, vld_tgt_hsp_list, vld_hsp_err_list, usr_tol_conc, cas_list]
    """

    usr_n, usr_tol_err_d, usr_tol_err_p, usr_tol_err_h, usr_tol_conc = specify_cand_parameter() # collect format-validated usr input parameters

    usr_tgt_hsp_list = specify_target() # in the order of d, p, h

    vld_hsp_err_list = [usr_tol_err_d, usr_tol_err_p, usr_tol_err_h] # list of tol_err d, p, h

    cas_list = cand_cas_list
    vld_tgt_hsp_list = usr_tgt_hsp_list
    vld_usr_n = usr_n

    to_continue_get_prmt = True
    while to_continue_get_prmt:

        print('Validating parameters...')
        print('Validating n...')
        
        n_check = sp_vld_chk.is_cand_list_longer_than_n(cas_list, vld_usr_n) # check if the length of candidate list is larger than or equal to n, if not, pop warning and return to specify n step

        # check if the target hsp is covered by all the solvent candidate, if not, pop warning saying mission impossible and ask if user want to reset candidate list or reset the target or quit

        print('Validating target HSP...')
        target_achievable_check = sp_vld_chk.is_target_achievable(db_info_list, cas_list, vld_tgt_hsp_list)

        if target_achievable_check is True and n_check is True: # valid check passed

            to_continue_get_prmt = False
        
        else:

            print('Please choose to reset the required parameters or add more solvent candidates.')

            valid_reset_option_list = ['r', 'reset', 'a', 'add', 'q', 'quit']

            reset_option = sp_rtxt.rm_spc(input(' [r] - reset \n [a] - add \n [q] - quit \n')).lower()

            if not sp_vld_chk.is_option_valid(valid_reset_option_list, reset_option):

                sp_vld_chk.invalid_input()
            
            elif reset_option in ['q', 'quit']:

                print('Confirm to quit?')
                to_finish_reset_opt = sp_vld_chk.finish_check()
                
                if to_finish_reset_opt is not True:

                    exit()
            
            elif reset_option in ['r', 'reset']:

                if target_achievable_check is False:

                    print('Please reset target HSP.')
                    vld_tgt_hsp_list = specify_target()

                if n_check is False:

                    print('Please reset n. (recommend 2 or 3)')
                    vld_usr_n = specify_n()
                
            elif reset_option in ['a', 'add']:

                updt_cas_list = sp_ed.edit_cand_list(cas_list) # edit current list if necessary

                db_cas_list = db_info_list[1][1] # extract all cas in the current db

                not_in_db_cas = sp_vld_chk.is_cas_in(updt_cas_list, db_cas_list) # find invalid cas that are not in the db

                final_db_cas_filt = sp_vld_chk.not_in_db_filt(updt_cas_list, not_in_db_cas) # filter out not_in_db_cas

                cas_list = final_db_cas_filt

    all_parameters = [vld_usr_n, vld_tgt_hsp_list, vld_hsp_err_list, usr_tol_conc, cas_list]
    
    return all_parameters