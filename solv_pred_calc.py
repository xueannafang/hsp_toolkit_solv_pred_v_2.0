import numpy as np
from scipy.linalg import pinv
import itertools
import solv_pred_fetch_info as sp_ftch_info

def mtrx_s_bf_comb(cand_cas_list, db_list):
    """
    construct the standard hsp matrix before combination
    """
    total_cand = len(cand_cas_list)
    s_bf_comb = np.ones((4, total_cand))
    cand_all_info = sp_ftch_info.fetch_idx_cas_hsp(cand_cas_list, db_list)
    all_db_idx_list = sp_ftch_info.fetch_sub_hsp(cand_all_info, 'idx')
    all_db_cas_list = sp_ftch_info.fetch_sub_hsp(cand_all_info, 'cas')
    all_d = sp_ftch_info.fetch_sub_hsp(cand_all_info, 'd')
    all_p = sp_ftch_info.fetch_sub_hsp(cand_all_info, 'p')
    all_h = sp_ftch_info.fetch_sub_hsp(cand_all_info, 'h')
    s_bf_comb[0] = all_d
    s_bf_comb[1] = all_p
    s_bf_comb[2] = all_h

    return [s_bf_comb, [all_db_idx_list, all_db_cas_list]]

def gen_idx(list_length):
    """
    convert a list with a given length into a list of index
    """
    i = 0
    n_idx_list = []
    for i in range(0, list_length):
        n_idx_list.append(i)

    return n_idx_list


def comb_idx(len_list, n):

    idx_list = gen_idx(len_list)

    all_comb_idx_list = []

    for comb in itertools.combinations(idx_list, n):
        all_comb_idx_list.append(list(comb))
    
    return all_comb_idx_list

def itrt_cand(cand_cas_list, db_list, n):

    mat_s_bf_comb = mtrx_s_bf_comb(cand_cas_list, db_list)[0]
    mat_s_bf_comb_arr_t = np.array(mat_s_bf_comb).transpose() # get ready to store column info

    db_idx_bf_comb_list = mtrx_s_bf_comb(cand_cas_list, db_list)[1][0]
    db_cas_bf_comb_list = mtrx_s_bf_comb(cand_cas_list, db_list)[1][1]

    all_comb_idx_list = comb_idx(len(db_idx_bf_comb_list), n)

    all_comb_mat_s_arr_t = []
    all_comb_mat_cas = []


    for comb_idx_grp in all_comb_idx_list:

        comb_for_s_arr_t = []
        comb_for_cas = []

        for i in range(0, n):
            
            idx = comb_idx_grp[i]
            comb_for_s_arr_t.append(mat_s_bf_comb_arr_t[idx])
            comb_for_cas.append(db_cas_bf_comb_list[idx])
        
        all_comb_mat_s_arr_t.append(comb_for_s_arr_t)
        all_comb_mat_cas.append(comb_for_cas)
    
    return all_comb_mat_s_arr_t, all_comb_mat_cas









    






    










     

