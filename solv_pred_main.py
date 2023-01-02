#import os
#import numpy as np
#import json

import solv_pred_io as sp_io
import solv_pred_gen_cand as sp_gen_cand
import solv_pred_cand_edit as sp_cand_ed
import solv_pred_valid_check as sp_vld_chk
import solv_pred_fetch_info as sp_ftch_info
import solv_pred_prmtr as sp_prmtr


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

    print('Step 2: Specify parameters. \n Please follow the instruction to specify the \n - Maximum number of solvents (n) to be included in each combination (default = 2); \n - Highest acceptable error of HSP (tol_err) of the predicted combination (default = 0.5); \n - Lowest acceptable concentration (tol_conc) of each predicted solvent component (default = 0.01). \n - Target HSP (target D, P, H). \n Temperature (default = 25 C). \n')

    temp_updt_db, is_temp_updt = sp_prmtr.specify_temp(db_full_info_list) #is_temp_updt = 1 will disable the follow up miscibility check
    usr_n, usr_tol_err_d, usr_tol_err_p, usr_tol_err_h, usr_tol_conc = sp_prmtr.specify_cand_parameter()
    usr_tgt_hsp_list = sp_prmtr.specify_target() # in the order of d, p, h
    #print(is_temp_updt, usr_tgt_hsp_list, usr_n, usr_tol_err_d, usr_tol_err_p, usr_tol_err_h, usr_tol_conc)

    #check if the length of candidate list is larger than or equal to n, if not, pop warning and return to specify n step or edit candidate list
    #check if the target hsp is covered by all the solvent candidate, if not, pop warning saying mission impossible and ask if user want to reset candidate list or reset the target or quit
    #this step needs to give each procedure an index and include everything in a big while true


    















solv_pred_main()



#input_cas()
#load_db("db_mis.json")
#generate_candidate_list('default_solv_candidate.json')