import solv_pred_valid_check as sp_vld_chk
import solv_pred_io as sp_io
import solv_pred_temp_update as sp_temp_updt
import solv_pred_reg_txt as sp_rtxt

def specify_parameter(orig_db_info_list):

    """
    Update temperature correction - a temperature-corrected database will be constructed in this step.
    """
    temp_corr_db_list = specify_temp(orig_db_info_list)

    """
    Specify n, tol_err, tol_conc
    """
    usr_n, usr_tol_err, usr_tol_conc = specify_cand_parameter()

    return [temp_corr_db_list, usr_n, usr_tol_err, usr_tol_conc] 

def specify_temp(orig_db_info_list):
    
    to_continue = True
    default_temp = 25

    while to_continue:

        valid_temp_confirm_list = ['t', 'c', 'continue', 'q', 'quit']
        temp_confirm = input('[t] - set a different temperature \n[c] - continue as room temperature (25 degree c). \n[q] - quit\n').lower()
        temp_edit = 0

        if not sp_vld_chk.is_option_valid(valid_temp_confirm_list, temp_confirm):
            sp_vld_chk.invalid_input()

        elif temp_confirm in ['t']:
            #further ask for required temperature, pop up a warning that solvents whose boiling point below this point will be removed, miscibility will not be considered, all the standard hsp will be updated.
            
            #invoke updating temperature function
            
            usr_target_temp = sp_rtxt.rm_spc(input('Please enter the target temperature (in degree C): '))
            usr_target_temp_is_float = sp_vld_chk.is_float(usr_target_temp) #check this is a float

            if usr_target_temp_is_float == False:
                sp_vld_chk.invalid_input()
                print('Please enter a valid number.')
            
            else:
                target_temp = float(usr_target_temp)
                
                if target_temp == default_temp:

                    print('25 C is the default temperature. \n Temperature correction will not be applied.')
                    db_temp_corr = orig_db_info_list
                    print('Continue?')
                    to_continue = sp_vld_chk.finish_check()
                
                else:
                    
                    print('Temperature has been set as: ' + usr_target_temp)

                    print('Applying temperature correction for standard HSP...')

                    db_temp_corr = sp_temp_updt.temp_corr_db(orig_db_info_list, 25, target_temp)
                    temp_edit = 1
                    
                    #db_temp_corr = sp_temp_updt.temp_updt_db(orig_db_info_list)
                    to_continue = False

        elif temp_confirm in ['c', 'continue']:
            # finish_check, then start setting the rest of parameters
            db_temp_corr = orig_db_info_list
            to_continue = False
        
        elif temp_confirm in ['q', 'quit']:
            exit()
    
    return [db_temp_corr, temp_edit]


def specify_cand_parameter():
    #check if usr wants to use default or not
    #to_specify_list = ['n', 'tol_err', 'tol_conc']
    usr_cand_parameter_default_list = [2, 0.5, 0.5, 0.5, 0.01] # in the order of n, tol_err, tol_conc
    usr_cand_parameter_list = []

    to_continue = True
    while to_continue:

        usr_set_option = input('Set parameters: \n[d] - use default settings for all parameters. \n[m] - manually set parameters. \n')
        valid_set_option_list = ['d', 'm', 'default', 'manual']
        usr_cand_parameter_list = []

        if not sp_vld_chk.is_option_valid(valid_set_option_list, usr_set_option):
            sp_vld_chk.invalid_input()
        
        elif usr_set_option in ['d', 'default']:
            usr_cand_parameter_list = usr_cand_parameter_default_list
            print('Default parameters will be applied.')
            print('Continue?')
            to_continue = sp_vld_chk.finish_check()
        
        elif usr_set_option in ['m', 'manual']:
            print('Please specify parameters.')
            
            print('n is the maximum number of solvents involved in each prediction.\nMust be a postivie integer >= 2.')
            usr_n = sp_rtxt.rm_spc(input('Please specify n: '))
            
            print('tolerance of error is the highest acceptable absolute error of HSP from the predicted solvent mixture. \n Must be a positive float.')
            usr_tol_err_d = sp_rtxt.rm_spc(input('Please specify tolerance of error for dispersion term (D): '))
            usr_tol_err_p = sp_rtxt.rm_spc(input('Please specify tolerance of error for dipolar term (P): '))
            usr_tol_err_h = sp_rtxt.rm_spc(input('Please specify tolerance of error for hydrogen bond term (H): '))
            
            print('lowest acceptable concentration is the threshold of predicted solvent concentration below which will be filtered out. \nMust be a float between 0 and 1. \n0 stands for 0%. 1 stands for 100%.')
            usr_tol_conc = sp_rtxt.rm_spc(input('Please specify lowest acceptable concentration: '))

            
            usr_n_valid = sp_vld_chk.is_n_vld(usr_n)
            usr_tol_err_d_valid = sp_vld_chk.is_tol_err_vld(usr_tol_err_d)
            usr_tol_err_p_valid = sp_vld_chk.is_tol_err_vld(usr_tol_err_p)
            usr_tol_err_h_valid = sp_vld_chk.is_tol_err_vld(usr_tol_err_h)
            usr_tol_conc_valid = sp_vld_chk.is_tol_conc_vld(usr_tol_conc)

            parameter_valid_check_list = [usr_n_valid, usr_tol_err_d_valid, usr_tol_err_p_valid, usr_tol_err_h_valid, usr_tol_conc_valid]
            
            if False not in parameter_valid_check_list:  # all
                usr_cand_parameter_list = [usr_n, usr_tol_err_d, usr_tol_err_p, usr_tol_err_h, usr_tol_conc]
                print('n, tol_err, tol_conc have been specified as: ')
                print(usr_cand_parameter_list)
                print('Continue?')
                to_continue = sp_vld_chk.finish_check()
            
    return usr_cand_parameter_list



def specify_target():

    usr_tgt_hsp_list = []
    to_continue = True

    while to_continue:

        print('target d, p, h are target HSPs to be achieved. \n Must be non-negative float.')
        usr_tgt_d = sp_rtxt.rm_spc(input('Please specify the target of dispersion term (target D): '))
        usr_tgt_p = sp_rtxt.rm_spc(input('Please specify the target of dispersion term (target P): '))
        usr_tgt_h = sp_rtxt.rm_spc(input('Please specify the target of dispersion term (target H): '))

        usr_tgt_d_valid = sp_vld_chk.is_tol_err_vld(usr_tgt_d)
        usr_tgt_p_valid = sp_vld_chk.is_tol_err_vld(usr_tgt_p)
        usr_tgt_h_valid = sp_vld_chk.is_tol_err_vld(usr_tgt_h)

        parameter_valid_check_list = [usr_tgt_d_valid, usr_tgt_p_valid, usr_tgt_h_valid]
            
        if False not in parameter_valid_check_list:  # all
            usr_tgt_hsp_list = [usr_tgt_d, usr_tgt_p, usr_tgt_h]
            print('target d, target p, target h have been specified as: ')
            print(usr_tgt_hsp_list)
            print('Continue?')
            to_continue = sp_vld_chk.finish_check()

    return usr_tgt_hsp_list
    

            










    return [n, tol_err, tol_conc]


"""
Results filtration step
"""
def specify_bp(low_bp_limit, high_bp_limit):
    pass