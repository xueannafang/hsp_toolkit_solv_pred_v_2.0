#import os
#import numpy as np
#import json

import solv_pred_io as sp_io
import solv_pred_gen_cand as sp_gen_cand
import solv_pred_cand_edit as sp_cand_ed
import solv_pred_valid_check as sp_vld_chk


def solv_pred_main(db = 'db_solv_pred_v2.json', default_candidate = 'default_solv_candidate.json'):

    print('Loading database and default candidate list...')
    
    db_js = sp_io.load_js(db)
    default_solv_candidate_js = sp_io.load_js(default_candidate)

    db_full_info_list = sp_io.db_init(db_js)
    db_cas_list = db_full_info_list[1][1]
    db_name_list = db_full_info_list[2][1]
    #print(db_cas_list, db_name_list)

    if db_js and default_solv_candidate_js:
        print('Database and default solvent candidate list has been loaded. \n Please follow the instruction to continue: ')
    
    usr_gen_cand_list = sp_gen_cand.generate_candidate_list(default_solv_candidate_js)

    usr_gen_cas_to_remove = sp_cand_ed.remove_cas()
    cannot_remove_list = sp_vld_chk.is_cas_in(usr_gen_cas_to_remove, usr_gen_cand_list)
    #check if cas to be removed is in the candidate list

    if len(cannot_remove_list) != 0:
        print('The following solvents are not included in the aforementioned solvent candidate list and will be ignored:')
        print(cannot_remove_list)
        valid_cas_to_remove = list(set(usr_gen_cas_to_remove) - set(cannot_remove_list))
        #print('The following solvents will be removed: ')
        #print(valid_cas_to_remove)
    else:
        valid_cas_to_remove = usr_gen_cas_to_remove
    
    cas_list_after_usr_filt = list(set(usr_gen_cand_list) - set(valid_cas_to_remove))

    not_in_db_cas_list = sp_vld_chk.is_cas_in(cas_list_after_usr_filt, db_cas_list)

    if len(not_in_db_cas_list) != 0:
        print('The following solvents are not included in the database and will be ignored: ')
        print(not_in_db_cas_list)
        cas_list_after_db_filt = list(set(cas_list_after_usr_filt) - set(not_in_db_cas_list))
    
    else:
        cas_list_after_db_filt = cas_list_after_usr_filt
    
    print('The following solvents will be considered as candidates: ')
    print(cas_list_after_db_filt)

    


    
    #check if cas is in the usr_gen_cand_list and in the db


solv_pred_main()



#input_cas()
#load_db("db_mis.json")
#generate_candidate_list('default_solv_candidate.json')