import solv_pred_valid_check as sp_vld_chk
import solv_pred_io as sp_io


def specify_parameter():

    print('Step 2: Specify parameters. \n Please follow the instruction to specify the \n 1) Maximum number of solvents (n) to be included in each combination (default = 2); \n 2) Highest acceptable error of HSP (tol_err) of the predicted combination (default = 0.5); \n 3) Lowest acceptable concentration (tol_conc) of each predicted solvent component (default = 0.01). \nThe default temperature is 25C. \n Press [t] to set a different temperature. \n')

    
    to_continue = True

    while to_continue:
        valid_temp_confirm_list = ['t', 'c', 'continue', 'q', 'quit']
        temp_confirm = input('[t] - set a different temperature \n[c] - continue as room temperature. \n[q] - quit').lower()

        if not sp_vld_chk.is_option_valid(valid_temp_confirm_list, temp_confirm):
            sp_vld_chk.invalid_input()

        elif temp_confirm in ['t']:
            #further ask for required temperature, pop up a warning that solvents whose boiling point below this point will be removed, immiscibility will not be considered, all the standard hsp will be updated.
            
            #invoice updating temperature function
            
            to_continue = False

        elif temp_confirm in ['c', 'continue']:
            # finish_check, then start setting the rest of parameters

            # print("Please submit CAS No. of solvents to be considered as candidates. Add one solvent at one time. Press [enter] to continue.")
            # usr_solv_candidate_cas_list = sp_io.input_cas()
            # candidate_cas_list = usr_solv_candidate_cas_list
            to_continue = False
        
        elif temp_confirm in ['q', 'quit']:
            exit()
