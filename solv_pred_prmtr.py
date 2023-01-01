import solv_pred_valid_check as sp_vld_chk
import solv_pred_io as sp_io
import solv_pred_temp_update as sp_temp_updt
import solv_pred_reg_txt as sp_rtxt

def specify_parameter(orig_db_info_list):

    print('Step 2: Specify parameters. \n Please follow the instruction to specify the \n 1) Maximum number of solvents (n) to be included in each combination (default = 2); \n 2) Highest acceptable error of HSP (tol_err) of the predicted combination (default = 0.5); \n 3) Lowest acceptable concentration (tol_conc) of each predicted solvent component (default = 0.01). \nThe default temperature is 25C. \n Press [t] to set a different temperature. \n')

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
        temp_confirm = input('[t] - set a different temperature \n[c] - continue as room temperature. \n[q] - quit').lower()

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
                    
                    #db_temp_corr = sp_temp_updt.temp_updt_db(orig_db_info_list)
                    to_continue = False

        elif temp_confirm in ['c', 'continue']:
            # finish_check, then start setting the rest of parameters
            db_temp_corr = orig_db_info_list
            to_continue = False
        
        elif temp_confirm in ['q', 'quit']:
            exit()
    
    return db_temp_corr


def specify_cand_parameter():
    #check if usr wants to use default or not
    to_specify_list = ['n', 'tol_err', 'tol_conc']
    n = input('Please specify n: ')
    tol_err = input('Please specify tolerance of error: ')
    tol_conc = input('Please specify lowest acceptable concentration: ')
    return [n, tol_err, tol_conc]


"""
Results filtration step
"""
def specify_bp(low_bp_limit, high_bp_limit):
    pass