#import os
#import numpy as np
#import json

import solv_pred_io as sp_io
import solv_pred_gen_cand as sp_gen_cand
import solv_pred_cand_edit as sp_cand_ed
import solv_pred_valid_check as sp_vld_chk
import solv_pred_fetch_info as sp_ftch_info
import solv_pred_prmtr as sp_prmtr
import solv_pred_calc as sp_clc


def solv_pred_main(db = 'db_solv_pred_v2.json', default_candidate = 'default_solv_candidate.json'):

    """
    Load database and default candidate list.
    """

    print('Loading database and default candidate list...')
    
    db_js = sp_io.load_js(db)
    default_solv_candidate_js = sp_io.load_js(default_candidate)

    db_full_info_list = sp_io.db_init(db_js)
    db_cas_list = db_full_info_list[1][1]
    #db_name_list = db_full_info_list[2][1]
    #print(db_cas_list, db_name_list)

    if db_js and default_solv_candidate_js:
        print('Database and default solvent candidate list has been loaded. \n Please follow the instruction to continue: ')
    
    
    """
    Step_1: Generate candidate list

    user can choose to use default candidate list and then remove unwanted solvents or add more (recommended).

    Alternatively, users can create the candidate list by entering the cas no. of desired solvents.
    For the [manual] add method, users need to bear in mind that the minimum number of solvents must larger than 2 and there will be more likely to fail the prediction if the region connected by the selected solvents does not cover the target hsp.

    """
    
    usr_gen_cand_list = sp_gen_cand.generate_candidate_list(default_solv_candidate_js)

    usr_gen_cas_to_remove = sp_cand_ed.remove_cas()

    print('Checking if any solvent is not on the candidate list...')

    after_usr_filt_cand_list = sp_vld_chk.can_be_removed_check(usr_gen_cas_to_remove, usr_gen_cand_list)
    #check if cas to be removed is in the candidate list

    print('Done. \n Checking if any solvent is not in the database...')

    not_in_db_cas = sp_vld_chk.is_cas_in(after_usr_filt_cand_list, db_cas_list)

    after_db_filt_cand_list = sp_vld_chk.not_in_db_filt(after_usr_filt_cand_list, not_in_db_cas)
    
    print('Done.')
    #print('\n The following solvents will be considered as candidates: ')
    #print(after_db_filt_cand_list)
    
    edited_cand_list = sp_cand_ed.edit_cand_list(after_db_filt_cand_list)

    not_in_db_cas_final = sp_vld_chk.is_cas_in(edited_cand_list, db_cas_list)

    final_db_cas_filt = sp_vld_chk.not_in_db_filt(edited_cand_list, not_in_db_cas_final)

    print('Candidate list has been successfully generated:')
    #print(final_db_cas_filt)

    final_db_name_filt = []

    for cas in final_db_cas_filt:
        matched_name = sp_ftch_info.fetch_name(cas, db_js)
        final_db_name_filt.append(matched_name)
    
    print(final_db_name_filt)


    """
    Step 2: Specify calculation parameters.

    user need to first specify the temperature - default temperature is 25 degree c.
    if temperature is edited, the database will be updated by applying temperature correction for the three HSP.

    user then need to specify the following parameters:

    n - maximum number of solvents involved in each combination. default n = 2. recommend to use 2 or 3.

    tol_err_d, p, h - tolerance of error of the calculated HSP based on the predicted combinations.
    Errors higher than these values will be filtered.

    tol_conc - threshold of lowest acceptable concentration of each solvent component.
    Solvents with predicted concentration below this value will be filtered.

    target_d, p, h - the target hsp to be achieved.
    This target must be included in the region connected by all the solvent candidates in the Hansen space.
    This version will automatically check if this requirement is met or not. 

    """

    print('=========================\nStep 2: Specify parameters. \n Please follow the instruction to specify the \n - Maximum number of solvents (n) to be included in each combination (default = 2); \n - Highest acceptable error of HSP (tol_err) of the predicted combination (default = 0.5); \n - Lowest acceptable concentration (tol_conc) of each predicted solvent component (default = 0.01). \n - Target HSP (target D, P, H). \n Temperature (default = 25 C). \n')

    temp_updt_db, is_temp_updt = sp_prmtr.specify_temp(db_full_info_list) #is_temp_updt = 1 will disable the follow up miscibility check
    
    all_parameters = sp_prmtr.get_parameter(final_db_cas_filt, temp_updt_db)
    print('Parameter selection done.\n')
    #print(all_parameters)

    n = all_parameters[0]
    target_hsp_list = all_parameters[1] # in the order of d, p, h
    tol_err_list = all_parameters[2] # in the order of tol_err_d, tol_err_p, tol_err_h
    tol_conc = all_parameters[3]
    cand_cas_for_calc_list = all_parameters[4]

    """
    Step 3

    Main calculation cell

    Iterate through all the combinations of n-nary solvent systems
    Construct standard HSP matrix based on n-candidate combination
    Construct target HSP matrix with statistical perturbation
    Statistical validation
    Rough filtration - concentration renormalisation - fine filtration
    """

    #print(temp_updt_db)
    #sp_clc.mtrx_s_bf_comb(cand_cas_for_calc_list, temp_updt_db)
    # sp_clc.itrt_cand(cand_cas_for_calc_list, temp_updt_db, n)

    sp_clc.calc_vld_all_c(cand_cas_for_calc_list, temp_updt_db, n, target_hsp_list, tol_err_list, tol_conc)


    

    


    """
    Step 4
    optional filtrations
    miscibility check
    bp check

    """
















solv_pred_main()



#input_cas()
#load_db("db_mis.json")
#generate_candidate_list('default_solv_candidate.json')