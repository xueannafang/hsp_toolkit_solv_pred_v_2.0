#import os
#import numpy as np
#import json

import solv_pred_io as sp_io
import solv_pred_gen_cand as sp_gen_cand
import solv_pred_cand_edit as sp_cand_ed
import solv_pred_valid_check as sp_vld_chk
import solv_pred_fetch_info as sp_ftch_info


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
    """
    
    
    usr_gen_cand_list = sp_gen_cand.generate_candidate_list(default_solv_candidate_js)

    usr_gen_cas_to_remove = sp_cand_ed.remove_cas()

    print('Checking if any solvent is not on the candidate list...')

    after_usr_filt_cand_list = sp_vld_chk.can_be_removed_check(usr_gen_cas_to_remove, usr_gen_cand_list)
    #check if cas to be removed is in the candidate list

    print('Done. \n Checking if any solvent is not in the database...')

    not_in_db_cas = sp_vld_chk.is_cas_in(after_usr_filt_cand_list, db_cas_list)

    after_db_filt_cand_list = sp_vld_chk.not_in_db_filt(after_usr_filt_cand_list, not_in_db_cas)
    
    print('Done. \n The following solvents will be considered as candidates: ')
    print(after_db_filt_cand_list)
    
    edited_cand_list = sp_cand_ed.edit_cand_list(after_db_filt_cand_list)

    not_in_db_cas_final = sp_vld_chk.is_cas_in(edited_cand_list, db_cas_list)

    final_db_cas_filt = sp_vld_chk.not_in_db_filt(edited_cand_list, not_in_db_cas_final)

    print('Candidate list successfully generated:')
    #print(final_db_cas_filt)

    final_db_name_filt = []

    for cas in final_db_cas_filt:
        matched_name = sp_ftch_info.fetch_name(cas, db_js)
        final_db_name_filt.append(matched_name)
    
    print(final_db_name_filt)


    """
    Step 2: Specify calculation parameters.
    """

    















solv_pred_main()



#input_cas()
#load_db("db_mis.json")
#generate_candidate_list('default_solv_candidate.json')