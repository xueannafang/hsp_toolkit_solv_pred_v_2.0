#import os
#import numpy as np
#import json

import solv_pred_io as sp_io
import solv_pred_gen_cand as sp_gen_cand


def solv_pred_main(db = 'db_solv_pred_v2.json', default_candidate = 'default_solv_candidate.json'):
    
    db_js = sp_io.load_js(db)
    default_solv_candidate_js = sp_io.load_js(default_candidate)
    
    sp_gen_cand.generate_candidate_list(default_solv_candidate_js)


solv_pred_main()



#input_cas()
#load_db("db_mis.json")
#generate_candidate_list('default_solv_candidate.json')